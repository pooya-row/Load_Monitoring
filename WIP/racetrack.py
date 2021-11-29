from matplotlib import pyplot as plt

from utils import get_data_np
import fatpack

# time = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
# signal = np.array([-2, 1, -3, 5, -1, 2, -4, 4, -1])

file_path = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder' \
            '\\Monday November 15, 2021 01-04 PM - Copy.dat'
time, signal = get_data_np.get_data(file_path, [7])

# ==================== racetrack filter ====================
# rev = []
# for i in rainflow.reversals(signal):
#     rev.append(i[1])

signal_rtf, ix_rtf = fatpack.find_reversals_racetrack_filtered(signal,
                                                               h=.15)

# signal_rtf, inx = fatpack.racetrack_filter(reversals=np.array(rev_rtf), h=.15)
time_rtf = time[ix_rtf]

print(f'raw = {len(time)}')
print(f'last raw = {time[-1]}')
print(f'filtered = {len(time_rtf)}')
print(f'last filtered = {time_rtf[-1]}')
print(ix_rtf)
for t, s in zip(time[:30], signal[:30]):
    print(f'{t[0]}, {s[0]}')
print()
for t, s in zip(time_rtf[:10], signal_rtf[:10]):
    print(f'{t[0]}, {s[0]}')

# instantiate plots
# fig, ax = plt.subplots(2, 1, figsize=(16, 8), constrained_layout=True)

# graphs.plot_signal(x=list(time), y=list(signal), marker='', ax=ax[0],
#                    print_label=True)
#
# ax[0].set_xlabel('')
# ax[0].set_ylabel('Load Units')
# ax[0].set_title('Raw Data', fontsize=15)
# ax[0].set_xlim((0, 1))
#
# graphs.plot_signal(x=list(time_rtf), y=list(signal_rtf), marker='',
#                    ax=ax[1], print_label=True)
# ax[1].set_ylabel('Load Units')
# ax[1].set_title('Filtered Data', fontsize=15)
# ax[1].set_xlim((0, 1))

# ax[1].grid(True)
# ax[0].set_xlabel('')
# ax[0].set_xticklabels('')
# ax[0].set_xticks([])
# ax[0].set_ylim((-6, 6))
# ax[1].set_xticklabels('')
# ax[1].set_xticks([])
# ax[1].set_ylim((-6, 6))

plt.plot(list(time), list(signal), linewidth=.5)  # ,
plt.plot(list(time_rtf), list(signal_rtf), linewidth=.5, c='g')  # ,
# ax[0].grid(True)
# ax[1].grid(True)
# linewidth=.5, color='xkcd:dark slate blue',
# # axes=ax,
# )

# # ==================== manage warning handling
# np.seterr(all='warn')
# warnings.filterwarnings(action='error')
#
# # call GUI, get user input
# mean_bin_size, range_bin_size, g_exc_bin_size, file_path, material, k_t = \
#     GUI.gui_single_file()
#
#
# # extract cycles and their properties - (n, 5)
# # columns = [mean, range, count, start, end]
# mean, rng, count, start_i, end_i = [], [], [], [], []
# for rg, mn, c, i_s, i_e in rainflow.extract_cycles(signal_rtf):
#     mean.append(mn)
#     rng.append(rg)
#     count.append(c)
#     start_i.append(signal_rtf[i_s])
#     end_i.append(signal_rtf[i_e])
#     # start_i.append(i_s)
#     # end_i.append(i_e)
#
# cycles = np.column_stack((mean, rng, count, start_i, end_i))
#
# # ==================== generate mean-range matrix ====================
# # mean_bin_size = .25
# # range_bin_size = .5
# mean_bin_edges = np.arange(np.floor(np.amin(cycles[:, 0])),
#                            np.ceil(np.amax(cycles[:, 0])) + mean_bin_size,
#                            mean_bin_size)
# range_bin_edges = np.arange(np.floor(np.amin(cycles[:, 1])),
#                             np.ceil(np.amax(cycles[:, 1])) + range_bin_size,
#                             range_bin_size)
#
# m_r_matrix = np.zeros((len(range_bin_edges) - 1, len(mean_bin_edges) - 1))
#
# for i in range(len(cycles)):
#     m = np.digitize(cycles[i, 0], mean_bin_edges, right=True) - 1
#     r = np.digitize(cycles[i, 1], range_bin_edges, right=True) - 1
#     m_r_matrix[r, m] += cycles[i, 2]
#
# # ==================== generate cycles-to-failure matrix ====================
# mean_bins = np.array(
#     [(i + j) / 2 for i, j in zip(mean_bin_edges[1:], mean_bin_edges[:-1])])
# range_bins = np.array(
#     [(i + j) / 2 for i, j in zip(range_bin_edges[1:], range_bin_edges[:-1])])
# N_matrix = np.zeros(m_r_matrix.shape)
# a, b, c, d = material_lib.property_selector(material, k_t)
#
# for i in range(N_matrix.shape[0]):
#     for j in range(N_matrix.shape[1]):
#         S_max = mean_bins[j] + range_bins[i] / 2
#         S_min = mean_bins[j] - range_bins[i] / 2
#
#         try:
#             R = S_min / S_max
#         except ValueError:
#             R = 0.
#
#         try:
#             S_eq = S_max * (1 - R) ** d
#         except ValueError:
#             R = 0.
#             S_eq = S_max * (1 - R) ** d
#
#         N_matrix[i, j] = 10 ** (a - b * np.log(S_eq + c))
# # TODO: the sign in the log argument must be negative log(S_eq - c)
#
# # ==================== damage ====================
# damage_matrix = m_r_matrix / N_matrix
# total_damage = damage_matrix.sum()
#
# # ==================== generate from-to matrix ====================
# from_bin_size = .5
# to_bin_size = .5
# from_bin_edges = np.arange(np.floor(np.amin(cycles[:, 3])),
#                            np.ceil(np.amax(cycles[:, 3])) + from_bin_size,
#                            from_bin_size)
# to_bin_edges = np.arange(np.floor(np.amin(cycles[:, 4])),
#                          np.ceil(np.amax(cycles[:, 4])) + to_bin_size,
#                          to_bin_size)
#
# from_to_matrix = np.zeros((len(to_bin_edges) - 1, len(from_bin_edges) - 1))
# for i in range(len(cycles)):
#     t = np.digitize(cycles[i, 4], to_bin_edges, right=True) - 1
#     f = np.digitize(cycles[i, 3], from_bin_edges, right=True) - 1
#     from_to_matrix[t, f] += cycles[i, 2]
#
# # ==================== reset warning handling ====================
# warnings.resetwarnings()
#
# for i in zip(rng, mean, start_i, end_i):
#     print(i)
#
# # ==================== plot signal ====================
#
# # plot mean-range matrix
# graphs.plot_rf_matrix(count_matrix=m_r_matrix, x=cycles[:, 0], y=cycles[:, 1],
#                       x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
#                       ax=ax[1, 0], color_map='crest', labels=True,
#                       tlt='Mean-Range Matrix', x_lbl='Mean', y_lbl='Range')
# # plot cycle to failure matrix
# graphs.plot_rf_matrix(count_matrix=N_matrix, x=cycles[:, 0], y=cycles[:, 1],
#                       x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
#                       ax=ax[1, 1], labels=True, color_map='jet',
#                       tlt='Cycle-to-Failure Matrix',
#                       x_lbl='Mean', y_lbl='Range')
# # plot damage matrix
# graphs.plot_rf_matrix(count_matrix=damage_matrix,
#                       x=cycles[:, 0], y=cycles[:, 1],
#                       x_bin_size=mean_bin_size, y_bin_size=range_bin_size,
#                       ax=ax[0, 1], labels=True, color_map='crest',
#                       tlt='Damage Matrix', x_lbl='Mean', y_lbl='Range')
# # plot from-to matrix
# # graphs.plot_rf_matrix(count_matrix=from_to_matrix, x=cycles[:, 3],
# # y=cycles[:, 4],
# #                       x_bin_size=from_bin_size, y_bin_size=to_bin_size,
# #                       ax=ax[2], labels=True,
# #                       tlt='From-To Matrix', x_lbl='From', y_lbl='To')
# # plt.savefig('signal.png', dpi=600)
plt.show()
