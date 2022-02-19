"""
This script applies a kernel of a given size over the raw data as a
reduction filter. Then moves the kernel over the reduction window. For each
case, it plots the exceedance curve. The resulting plot is useful in the
impact study of the reduction filter when throwing away data.
"""

import math

import numpy as np
import rainflow
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.ticker import LogFormatterSciNotation, MultipleLocator

from utils import get_data_np, level_crossing, graphs

sns.set_theme(style='whitegrid', palette='colorblind',
              font='DejaVu Sans', font_scale=.6)

file_path = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\' \
            'salvaged\\Friday September 24, 2021 06-34 AM_TimeAdded.dat'

data = get_data_np.get_data(file_path, [7])
# nz = np.array(data[1]).reshape(-1)

window_size = 10
temp = range(len(data[0]))
print(len(data[0]))

fig, ax = plt.subplots(dpi=200, figsize=(9, 7))
plt.subplots_adjust(top=.93, bottom=.08, left=.08, right=.95)

for i in range(window_size):
    t = [data[0][var] for var in temp if var % 10 == i]
    nz = np.array([data[1][var] for var in temp if var % 10 == i]).reshape(-1)

    cyc_prop = {
        'cyc_mean': [], 'cyc_range': [], 'cyc_count': [],
        'start_i': [], 'end_i': [],
        'peak': [], 'valley': []}

    for rg, mn, c, i_s, i_e in rainflow.extract_cycles(nz):
        cyc_prop['cyc_mean'].append(mn)
        cyc_prop['cyc_range'].append(rg)
        cyc_prop['cyc_count'].append(c)
        cyc_prop['start_i'].append(nz[i_s])
        cyc_prop['end_i'].append(nz[i_e])
        cyc_prop['peak'].append(mn + rg / 2)
        cyc_prop['valley'].append(mn - rg / 2)

    cycles = np.column_stack(
        (cyc_prop['cyc_count'], cyc_prop['peak'], cyc_prop['valley']))

    top_bins, bottom_bins, top_counts, bottom_counts \
        = level_crossing.level_cross_count(cycles, .002)

    ax.plot(bottom_bins[::-1] + top_bins,
            np.concatenate((bottom_counts[::-1], top_counts)),
            label=i, linewidth=0.6)
    y_max = max(max(top_counts), max(bottom_counts))
    y_lim = 10 ** (math.ceil(math.log(y_max, 10)))
    ax.set_ylim((0.1, y_lim))

ax.axvline(1, c='r', linestyle='--')

ax.set_yscale('log')
ax.grid(which='both', linewidth=0.3, alpha=0.6)
ax.spines[:].set_color('black')
ax.spines[:].set_linewidth(0.5)
ax.yaxis.set_minor_formatter(
    LogFormatterSciNotation(labelOnlyBase=False,
                            minor_thresholds=(7, 0.1)))
ax.xaxis.set_major_locator(MultipleLocator(0.1))
ax.legend(fontsize=10)
ax.set_title(f'1 out of {window_size} points: {100 / window_size} Hz',
             fontsize=11)
plt.show()
