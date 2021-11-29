import rainflow
from pprint import pprint
import numpy as np
from math import ceil, floor
from utils import graphs
from WIP import signal_gen


def add_one(x):
    return x + 1


# user defined parameters
interval_length = 0.5
base_g = 1

# produce signal
time, signal = signal_gen.produce_signal(400, .06, base_g, 42)

# record reversals
reversals = [x for x in rainflow.reversals(signal)]
print('\nReversals')
pprint([x for x in reversals])

# largest and smallest signals
max_signal = max([x[1] for x in reversals])
min_signal = min([x[1] for x in reversals])

# intervals above baseline
if (max_signal - base_g) % interval_length != 0.0:
    top_intervals = ceil((max_signal - base_g) / interval_length)
else:  # reversal exactly on a bin border
    top_intervals = ceil((max_signal - base_g) / interval_length) + 1
# intervals below baseline
if (min_signal - base_g) % interval_length != 0.0:
    bottom_intervals = int(abs(floor((min_signal - base_g) / interval_length)))
else:  # reversal exactly on a bin border
    bottom_intervals = int(abs(floor((min_signal - base_g) / interval_length))) + 1

# print absolute peak and valley
print(f'\nMaximum Signal: {max_signal:.4f}\nNo. of Intervals above baseline: {top_intervals}'
      f'\n\nMinimum Signal: {min_signal:.4f}\nNo. of Intervals below baseline: {bottom_intervals}')

# initiate counters and binners
tops = np.zeros(top_intervals)
bots = np.zeros(bottom_intervals)
top_bins = [round(base_g + interval_length * (2 * i + 1) / 2, 5) for i in range(top_intervals)]
bot_bins = [round(base_g - interval_length * (2 * i + 1) / 2, 5) for i in range(bottom_intervals)]

for k, n_z in reversals:

    # exclude head and tail
    if k == 0 or k == len(signal) - 1:
        continue

    # count reversals above baseline
    if n_z >= base_g:
        i = 0
        while n_z >= base_g + i * interval_length:
            i += 1
        tops[:i] = list(map(add_one, tops[:i]))

    # count reversals below baseline
    else:
        i = 0
        while n_z <= base_g - i * interval_length:
            i += 1
        bots[:i] = list(map(add_one, bots[:i]))

# print numbers of level-crossings
print(f'\nTops\t\t= {[int(i) for i in tops]}\nTop Bins\t= {top_bins}'
      f'\n\nBottoms\t\t= {[int(i) for i in bots]}\nBottom Bins\t= {bot_bins}')

# generate graphs
graphs.plot_g_exc(time, signal, base_g,
                  tops, top_bins, bots, bot_bins,
                  print_label=False, print_bins=True, save_fig=False)

