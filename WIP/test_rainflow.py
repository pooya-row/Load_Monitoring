import numpy as np
import rainflow
from pprint import pprint

from matplotlib import pyplot as plt

from WIP import signal_gen

# produce signal
time, signal = signal_gen.produce_signal(400, .01, 1., 42)

bin_size = 1

# print a few parameters
# print('\nDefault')
# pprint(rainflow.count_cycles(signal))
# print(sum([x[1] for x in rainflow.count_cycles(signal)]))
# print('\n\nNumber of digits = 2')
# pprint(rainflow.count_cycles(signal, ndigits=1))
# print('\n')
print(f'\n\nBin size = {bin_size}\n')
pprint(rainflow.count_cycles(signal, binsize=bin_size))

# print loops information
range_list = []
print('\n\nLoops Details:\nRange\t|\tMean\t|\tCount\t| StartID\t|\tEndID\t| Start Signal\t|\tEnd signal')
for rng, mean, count, i_start, i_end in rainflow.extract_cycles(signal):
    # print(
    #     f'{rng:.4f}\t|\t{mean:.4f}\t|\t{count}\t\t|\t{i_start:2d}\t\t|\t\t{i_end:2d}\t|\t'
    #     f'{signal[i_start]:.4f}\t\t|\t{signal[i_end]:.4f}')
    range_list.append(rng)

# format print reversals
# print('\n\nReversals:')
# print('PointID\t|\tSignal')
# for n, i in rainflow.reversals(signal):
#     print(f'{n:3d}\t\t|\t{i:.5f}')

# generate plots
cycles = rainflow.count_cycles(signal, binsize=bin_size)
ranges = [round(i[0], 5) for i in cycles]
cycle_counts = [i[1] for i in cycles]

mean, rng, count, start_i, end_i = [], [], [], [], []
for r, m, c, i_s, i_e in rainflow.extract_cycles(signal):
    mean.append(r)
    rng.append(m)
    count.append(c)
    start_i.append(signal[i_s])
    end_i.append(signal[i_e])

data = np.column_stack((rng, mean, count, start_i, end_i))

# print(data.shape)
# print(len(data))
print()
# print(f'data\n{data}')
print()
mean_bin_size = .15
range_bin_size = .25
mean_bin_edges = np.arange(np.floor(np.amin(data[:, 0])), np.ceil(np.amax(data[:, 0])) + mean_bin_size, mean_bin_size)
range_bin_edges = np.arange(np.floor(np.amin(data[:, 1])), np.ceil(np.amax(data[:, 1])) + range_bin_size,
                            range_bin_size)
# print(np.ceil(np.amax(data[:,1])))
print(len(mean_bin_edges))
# print(range_bin_edges)

m_r_matrix = np.zeros((len(range_bin_edges) - 1, len(mean_bin_edges) - 1))

# print(m_r_matrix.shape)
# print(data[133:137, :])
# print(np.digitize(data[135, 1], range_bin_edges, right=True) - 1)

for i in range(len(data)):
    m = np.digitize(data[i, 0], mean_bin_edges, right=True) - 1
    r = np.digitize(data[i, 1], range_bin_edges, right=True) - 1
    m_r_matrix[r, m] += data[i, 2]
print()
pprint(m_r_matrix)

from_bin_size = .25
to_bin_size = .25
from_bin_edges = np.arange(np.floor(np.amin(data[:, 3])), np.ceil(np.amax(data[:, 3])) + from_bin_size, from_bin_size)
to_bin_edges = np.arange(np.floor(np.amin(data[:, 4])), np.ceil(np.amax(data[:, 4])) + to_bin_size, to_bin_size)

from_to_matrix = np.zeros((len(from_bin_edges) - 1, len(to_bin_edges) - 1))

for i in range(len(data)):
    m = np.digitize(data[i, 3], from_bin_edges, right=True) - 1
    r = np.digitize(data[i, 4], to_bin_edges, right=True) - 1
    from_to_matrix[r, m] += data[i, 2]

# graphs.plot_rainflow(time, signal, ranges, cycle_counts, bin_size, print_label=False)

fig, ax = plt.subplots()
# x, y = np.meshgrid(mean_bin, range_bin, indexing='ij')
# c_mesh = ax.pcolormesh(mean_bin_edges, range_bin_edges, m_r_matrix, cmap='jet')
c_mesh = ax.pcolormesh(from_bin_edges, to_bin_edges, from_to_matrix, cmap='crest')
plt.colorbar(c_mesh, ax=ax)
# ax.set_xlabel('Mean')
# ax.set_ylabel('Range')
plt.show()
