import numpy as np
import matplotlib.pyplot as plt
import fatpack
import rainflow
import seaborn as sns

from WIP import signal_gen

# produce signal
time, signal = signal_gen.produce_signal(.4, .01, 1., 42)

# Find reversals (peaks and valleys), extract cycles and residue (open cycle
# sequence), process and extract closed cycles from residue.
reversals, reversals_ix = fatpack.find_reversals(signal, k=10000)
cycles, residue = fatpack.find_rainflow_cycles(reversals)
processed_residue = fatpack.concatenate_reversals(residue, residue)
cycles_residue, _ = fatpack.find_rainflow_cycles(processed_residue)
cycles_total = np.concatenate((cycles, cycles_residue))

# Find the rainflow ranges from the cycles
ranges = np.abs(cycles_total[:, 1] - cycles_total[:, 0])

N, S = fatpack.find_range_count(ranges, 64)
Ncum = N.sum() - np.cumsum(N)

Sa, Sm = fatpack.find_rainflow_ranges(signal, return_means=True, k=256)

row_bin = np.linspace(-25, 25, 50)
col_bin = np.linspace(0, 85, 50)

data_arr = np.array([Sm, Sa]).T
rfc_mat = fatpack.find_rainflow_matrix(data_arr, row_bin, col_bin)

X, Y = np.meshgrid(row_bin, col_bin, indexing='ij')
C = plt.pcolormesh(X, Y, rfc_mat, cmap='jet')
plt.colorbar(C)
plt.title("Rainflow matrix")
plt.xlabel("Mean")
plt.ylabel("Range")

print(cycles_total)
print(cycles_residue)
# for n, i in zip(reversals_ix, reversals):
#     print(f'{n:3d}\t\t|\t{i:.5f}')


# print loops information
range_list = []
print('\n\nLoops Details:\nRange\t|\tMean\t|\tCount\t| StartID\t|\tEndID\t| Start Signal\t|\tEnd signal')
for rng, mean, count, i_start, i_end in rainflow.extract_cycles(signal):
    print(
        f'{rng:.4f}\t|\t{mean:.4f}\t|\t{count}\t\t|\t{i_start:2d}\t\t|\t\t{i_end:2d}\t|\t'
        f'{signal[i_start]:.4f}\t\t|\t{signal[i_end]:.4f}')
    range_list.append(rng)

# format print reversals
print('\n\nReversals:')
print('PointID\t|\tSignal')
for n, i in rainflow.reversals(signal):
    print(f'{n:3d}\t\t|\t{i:.5f}')

fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=120)
plt.subplots_adjust(wspace=.27, bottom=0.15, top=.95, right=.98, left=0.1)

sns.lineplot(ax=axes[0], x=time, y=signal, linewidth=0.5, color='xkcd:dark slate blue')
axes[0].grid()

# i = 0
# for x, y in zip(time, signal):
#     # label = "{:.2f}".format(y)
#
#     plt.annotate(f'{i}, {y:.4f}',  # this is the text
#                  (x, y),  # this is the point to label
#                  textcoords="offset points",  # how to position the text
#                  xytext=(0, 3),  # distance from text to points (x,y)
#                  ha='center')  # horizontal alignment can be left, right or center
#     i += 1

plt.show()
