import numpy as np
import matplotlib.pyplot as plt
import fatpack

from utils import graphs
from WIP import signal_gen

resolution = 36

# produce signal
time, signal = signal_gen.produce_signal(400, .01, 1., 42)

# instantiate the plots
fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=120)
plt.subplots_adjust(hspace=.3, wspace=.27, bottom=0.075, top=.95, right=.98, left=0.09)

# plot signal data
graphs.plot_signal(x=time, y=signal, ax=axes[0, 0])

# rainflow count
Sa, Sm = fatpack.find_rainflow_ranges(signal, return_means=True, k=10000)
fatpack.find_reversals_racetrack_filtered()
# cumulative count
range_bins = np.linspace(0, np.ceil(max(Sa)), 101)
N, S = fatpack.find_range_count(Sa, range_bins)
Ncum = N.sum() - np.cumsum(N)
axes[0, 1].loglog(Ncum, S, 'k')
axes[0, 1].grid(which='both', alpha=.3, linewidth=0.4)
# axes[0, 1].bar(S, N, alpha=.5, width=range_bins[1] - range_bins[0])
axes[0, 1].set_title('Cumulative Range Counts', fontsize=13)
axes[0, 1].set_xlabel('Cumulative Count', fontsize=11)
axes[0, 1].set_ylabel('Rainflow Range [g]', fontsize=11)

# plot mean-range matrix
Sm_bins = np.linspace(np.floor(min(Sm)), np.ceil(max(Sm)), resolution)
Sa_bins = np.linspace(np.floor(min(Sa)), np.ceil(max(Sa)), resolution)
data_arr = np.array([Sm, Sa]).T
rfc_mat = fatpack.find_rainflow_matrix(data_arr, Sm_bins, Sa_bins)
graphs.mean_range_matrix_plot(data=data_arr, rf_matrix=rfc_mat, ax=axes[1, 0], labels=False)
print(data_arr)

# from-to rainflow matrix
rev, ix = fatpack.find_reversals(signal, k=256)
cyc1, res = fatpack.find_rainflow_cycles(rev)
rev_res = fatpack.concatenate_reversals(res, res)
cyc_res, _ = fatpack.find_rainflow_cycles(rev_res)
cycles = np.concatenate((cyc1, cyc_res))

a_min, a_max = np.floor(np.amin(cycles)), np.ceil(np.amax(cycles))
bins = np.linspace(a_min, a_max, resolution)
from_to_mtx = fatpack.find_rainflow_matrix(cycles, bins, bins)

# plot from-to matrix
graphs.from_to_matrix_plot(data=cycles, from_to_matrix=from_to_mtx, ax=axes[1, 1], labels=False)

# plt.savefig('gg.png', dpi=300)

plt.show()
