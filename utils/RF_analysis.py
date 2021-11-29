# import PySimpleGUIWx
import numpy as np
import rainflow
from matplotlib import pyplot as plt
# import PySimpleGUI as Sg
import graphs
import warnings
from utils import GUI, get_data_np
import level_crossing
import material_lib
from datetime import datetime

# manage warning handling
np.seterr(all='warn')
warnings.filterwarnings(action='error')

# call GUI, get user input
mean_bin_size, range_bin_size, gExc_bin_size, file_path, material, k_t = \
    GUI.gui_single_file()

# read data
t0 = datetime.now()
time, n_z = get_data_np.get_data(file_path, [7])
# data = get_data_np.get_data(file_path)
# time = data[:, 0].reshape(-1, 1)
# signal = data[:, 1].reshape(-1, 1)
# time = np.genfromtxt(file_path, delimiter=',')[:, 0]
# signal = np.genfromtxt(file_path, delimiter=',')[:, 1]
print(f'Collapsed time to load data: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')
print(time.shape)

# extract cycles and their properties - (n, 5)
# - columns = [mean, range, count, start, end]
t0 = datetime.now()
mean, rng, count, start_i, end_i, peak, valley = [], [], [], [], [], [], []
for rg, mn, c, i_s, i_e in rainflow.extract_cycles(n_z):
    mean.append(mn)
    rng.append(rg)
    count.append(c)
    start_i.append(n_z[i_s])
    end_i.append(n_z[i_e])
    peak.append(mn + rg / 2)
    valley.append(mn - rg / 2)
print(f'Collapsed time to extract cycles: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

cycles = np.column_stack((mean, rng, count, peak, valley))
print(cycles.shape)
# ==================== generate mean-range matrix ====================
t0 = datetime.now()
mean_bin_edges = np.arange(np.floor(np.amin(cycles[:, 0])),
                           np.ceil(np.amax(cycles[:, 0])) + mean_bin_size,
                           mean_bin_size)
range_bin_edges = np.arange(np.floor(np.amin(cycles[:, 1])),
                            np.ceil(np.amax(cycles[:, 1])) + range_bin_size,
                            range_bin_size)

m_r_matrix = np.zeros((len(range_bin_edges) - 1, len(mean_bin_edges) - 1))

for i in range(len(cycles)):
    m = np.digitize(cycles[i, 0], mean_bin_edges, right=True) - 1
    r = np.digitize(cycles[i, 1], range_bin_edges, right=True) - 1
    m_r_matrix[r, m] += cycles[i, 2]
print(f'Collapsed time to generate mean-range matrix: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# ==================== generate cycles-to-failure matrix ====================
t0 = datetime.now()
mean_bins = np.array(
    [(i + j) / 2 for i, j in zip(mean_bin_edges[1:], mean_bin_edges[:-1])])
range_bins = np.array(
    [(i + j) / 2 for i, j in zip(range_bin_edges[1:], range_bin_edges[:-1])])
N_matrix = np.zeros(m_r_matrix.shape)
a, b, c, d = material_lib.property_selector(material, k_t)

for i in range(N_matrix.shape[0]):
    for j in range(N_matrix.shape[1]):
        S_max = mean_bins[j] + range_bins[i] / 2
        S_min = mean_bins[j] - range_bins[i] / 2

        try:
            R = S_min / S_max
        except ValueError:
            R = 0.

        try:
            S_eq = S_max * (1 - R) ** d
        except ValueError:
            R = 0.
            S_eq = S_max * (1 - R) ** d

        # TODO: the sign in the log argument must be negative log(S_eq - c)
        N_matrix[i, j] = 10 ** (a - b * np.log(abs(S_eq) + c))
print(f'Collapsed time to extract cycles-to-failure matrix: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# ==================== damage ====================
damage_matrix = m_r_matrix / N_matrix
total_damage = damage_matrix.sum()
# Sg.popup(f'The total cumulative damage is {round(total_damage, 2)}.',
#          title='Total Damage', font=('Microsoft YaHei UI', 11),
#          background_color='#C2C2C2', text_color='black',
#          button_color=('#FFFFFF', '#283B5B'))

# ==================== generate from-to matrix ====================
t0 = datetime.now()
from_bin_size = .5
to_bin_size = .5
from_bin_edges = np.arange(np.floor(np.amin(cycles[:, 3])),
                           np.ceil(np.amax(cycles[:, 3])) + from_bin_size,
                           from_bin_size)
to_bin_edges = np.arange(np.floor(np.amin(cycles[:, 4])),
                         np.ceil(np.amax(cycles[:, 4])) + to_bin_size,
                         to_bin_size)

from_to_matrix = np.zeros((len(to_bin_edges) - 1, len(from_bin_edges) - 1))
for i in range(len(cycles)):
    t = np.digitize(cycles[i, 4], to_bin_edges, right=True) - 1
    f = np.digitize(cycles[i, 3], from_bin_edges, right=True) - 1
    from_to_matrix[t, f] += cycles[i, 2]
print(f'Collapsed time to generate from-to matrix: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# ==================== level cross counting ====================
t0 = datetime.now()
top_bins, bottom_bins, top_counts, bottom_counts = \
    level_crossing.level_cross_count(cycles[:, 2:], gExc_bin_size)
print(f'Collapsed time to complete level-crossing: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')
# print(f'Top bins:\n{top_bins}\n\n, Top counts:\n{top_counts}\n\n,'
#       f'Bottom bins:\n{bottom_bins}\n\n, Bottom counts:\n{bottom_counts}')

# ==================== reset warning handling ====================
warnings.resetwarnings()

# ==================== plot signal ====================
# instantiate plots
fig, ax = plt.subplots(2, 2, figsize=(16, 10))
plt.subplots_adjust(hspace=.3, wspace=.27,
                    bottom=0.1, top=.95, right=.98, left=0.06)

t0 = datetime.now()
graphs.plot_signal(x=time, y=n_z, ax=ax[0, 0])
print(f'Collapsed time to plot signal: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# plot mean-range matrix
t0 = datetime.now()
graphs.plot_rf_matrix(count_matrix=m_r_matrix, x=cycles[:, 0], y=cycles[:, 1],
                      x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
                      ax=ax[0, 1], color_map='jet', labels=False,
                      tlt='Mean-Amplitude Matrix',
                      x_lbl='Mean', y_lbl='Amplitude')
print(f'Collapsed time to plot mean-range: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# plot g-exceedance
t0 = datetime.now()
graphs.g_exceedance_plot(top_bins=top_bins, top_counts=top_counts,
                         bottom_bins=bottom_bins, bottom_counts=bottom_counts,
                         title='set', x_label='set', y_label='set',
                         print_label=False, print_bins=False,
                         ax=ax[1, 0])
print(f'Collapsed time to plot g-exceedance: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# plot damage matrix
t0 = datetime.now()
graphs.plot_rf_matrix(count_matrix=damage_matrix,
                      x=cycles[:, 0], y=cycles[:, 1],
                      x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
                      ax=ax[1, 1], labels=False, color_map='crest',
                      tlt='Damage Matrix', x_lbl='Mean', y_lbl='Range')

print(f'Collapsed time to plot damage matrix: '
      f'{(datetime.now() - t0).total_seconds()} sec\n')

# ==========
# plot cycle to failure matrix
# graphs.plot_rf_matrix(count_matrix=N_matrix, x=cycles[:, 0], y=cycles[:, 1],
#                       x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
#                       ax=ax[1, 1], labels=True, color_map='jet',
#                       tlt='Cycle-to-Failure Matrix', x_lbl='Mean',
#                       y_lbl='Range')
# plot from-to matrix
# graphs.plot_rf_matrix(count_matrix=from_to_matrix, x=cycles[:, 3],
# y=cycles[:, 4],
#                       x_bin_size=from_bin_size, y_bin_size=to_bin_size,
#                       ax=ax[2], labels=True,
#                       tlt='From-To Matrix', x_lbl='From', y_lbl='To')
# ==========

# ff, aa = plt.subplots()
# graphs.g_exceedance_plot(top_bins=top_bins, tops=top_counts,
#                          bottom_bins=bottom_bins, bottoms=bottom_counts,
#                          print_label=True, print_bins=False,
#                          ax=aa)
# graphs.plot_signal(x=time, y=n_z, ax=aa)
plt.show()
# ff.savefig('signal.png', dpi=300)

# import plotly.express as px
#
# x_bin_edges = np.arange(np.floor(np.amin(cycles[:, 0])),
# np.ceil(np.amax(cycles[:, 0])), mean_bin_size)
# y_bin_edges = np.arange(np.floor(np.amin(cycles[:, 1])),
# np.ceil(np.amax(cycles[:, 1])), range_bin_size)
# fig1 = px.imshow(damage_matrix, x=x_bin_edges, y=y_bin_edges,
# color_continuous_scale='peach')
# # line(x=time[:, 0], y=n_z[:, 0])
# fig1.show()
