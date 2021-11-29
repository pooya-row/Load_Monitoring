import numpy as np
import rainflow
from matplotlib import pyplot as plt

import warnings
from utils.matrices import GUI
from utils import material_lib, graphs

"""
Use the following parameters to generate the exact results as ASME example.
    Mean bin size = 0.5
    Range bin size = 1.
    g-exceedance Resolution = any
"""

time = np.array([0.848920863, 1.309352518, 2.007194245, 3.230215827, 4.18705036,
                 4.73381295, 5.985611511, 7.366906475, 8.165467626])
signal = np.array([-1.951672862, 0.789962825, -2.778810409, 4.823420074, -0.94795539,
                   2.79739777, -3.847583643, 3.884758364, -2.100371747])
signal -= .0743  # adjusting for the digitizing offset error

# manage warning handling
np.seterr(all='warn')
warnings.filterwarnings(action='error')

# call GUI, get user input
mean_bin_size, range_bin_size, ge_bin_size, file_path, material, k_t = GUI.gui_single_file()

# instantiate plots
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
plt.subplots_adjust(hspace=.3, wspace=.27, bottom=0.1, top=.95, right=.98, left=0.085)

# extract cycles and their properties - (n, 5) - columns = [mean, range, count, start, end]
mean, rng, count, start_i, end_i = [], [], [], [], []
for rg, mn, c, i_s, i_e in rainflow.extract_cycles(signal):
    mean.append(mn)
    rng.append(rg)
    count.append(c)
    start_i.append(signal[i_s])
    end_i.append(signal[i_e])
    # start_i.append(i_s)
    # end_i.append(i_e)

cycles = np.column_stack((mean, rng, count, start_i, end_i))

# ==================== generate mean-range matrix ====================
# mean_bin_size = .25
# range_bin_size = .5
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

# ==================== generate cycles-to-failure matrix ====================
mean_bins = np.array([(i + j) / 2 for i, j in zip(mean_bin_edges[1:], mean_bin_edges[:-1])])
range_bins = np.array([(i + j) / 2 for i, j in zip(range_bin_edges[1:], range_bin_edges[:-1])])
N_matrix = np.zeros(m_r_matrix.shape)
a, b, c, d = material_lib.property_selector(material, k_t)

for i in range(N_matrix.shape[0]):
    for j in range(N_matrix.shape[1]):
        S_max = mean_bins[j] + range_bins[i] / 2
        S_min = mean_bins[j] - range_bins[i] / 2

        try:
            R = S_min / S_max
        except:
            R = 0.

        try:
            S_eq = S_max * (1 - R) ** d
        except:
            R = 0.
            S_eq = S_max * (1 - R) ** d

        N_matrix[i, j] = 10 ** (a - b * np.log(S_eq + c))
# TODO: the sign in the log argument must be negative log(S_eq - c)

# ==================== damage ====================
damage_matrix = m_r_matrix / N_matrix
total_damage = damage_matrix.sum()

# ==================== generate from-to matrix ====================
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

# ==================== reset warning handling ====================
warnings.resetwarnings()

for i in zip(rng, mean, start_i, end_i):
    print(i)
# ==================== plot signal ====================
graphs.plot_signal(x=list(time), y=list(signal), ax=ax[0, 0], print_label=True)
ax[0, 0].set_xlabel('Time')
ax[0, 0].set_ylabel('Load Units')
ax[0, 0].set_title('Signal Data')
ax[0, 0].set_xticklabels('')
ax[0, 0].set_xticks([])
ax[0, 0].set_ylim((-6, 6))
# plot mean-range matrix
graphs.plot_rf_matrix(count_matrix=m_r_matrix, x=cycles[:, 0], y=cycles[:, 1],
                      x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
                      ax=ax[1, 0], color_map='crest', labels=True,
                      tlt='Mean-Amplitude Matrix', x_lbl='Mean', y_lbl='Amplitude')
# plot cycle to failure matrix
graphs.plot_rf_matrix(count_matrix=N_matrix, x=cycles[:, 0], y=cycles[:, 1],
                      x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
                      ax=ax[1, 1], labels=True, color_map='jet',
                      tlt='Cycle-to-Failure Matrix', x_lbl='Mean', y_lbl='Range')
# plot damage matrix
graphs.plot_rf_matrix(count_matrix=damage_matrix, x=cycles[:, 0], y=cycles[:, 1],
                      x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
                      ax=ax[0, 1], labels=True, color_map='crest',
                      tlt='Damage Matrix', x_lbl='Mean', y_lbl='Range')
# plot from-to matrix
# graphs.plot_rf_matrix(count_matrix=from_to_matrix, x=cycles[:, 3], y=cycles[:, 4],
#                       x_bin_size=from_bin_size, y_bin_size=to_bin_size,
#                       ax=ax[2], labels=True,
#                       tlt='From-To Matrix', x_lbl='From', y_lbl='To')
# plt.savefig('signal.png', dpi=600)
plt.show()
