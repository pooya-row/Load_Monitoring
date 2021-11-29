from math import floor, ceil

import numpy as np


def level_cross_count(signal: np.ndarray,
                      level_width: float,
                      base_g: float = 1.) -> (list, list, np.ndarray,
                                              np.ndarray):
    """
    Count the level crossing given a baseline, resolution, and an (n x 3)
    array containing counts, max and min of each cycle type.

    :param signal: `(n x 3)` array. Each row represents a type of cycle.
     First column is the counts of that cycle type, resulted from rainflow
     counting. Second column is the maximum value of that cycle family and
     the third column is the minimum value of that cycle family.
    :param level_width: Width of the desired levels
    :param base_g: Baseline

    :return: two lists containing the bins above and below baseline,
     and two arrays containing the counts of each bin above and below baseline.
    """

    # largest and smallest signals
    max_signal = max(signal[:, 1])
    min_signal = min(signal[:, 2])

    # intervals above baseline
    if (max_signal - base_g) % level_width != 0.0:
        top_intervals = ceil((max_signal - base_g) / level_width)
    else:  # reversal exactly on a bin border
        top_intervals = ceil((max_signal - base_g) / level_width) + 1
    # intervals below baseline
    if (min_signal - base_g) % level_width != 0.0:
        bottom_intervals = int(abs(floor((min_signal - base_g) / level_width)))
    else:  # reversal exactly on a bin border
        bottom_intervals = int(
            abs(floor((min_signal - base_g) / level_width))) + 1

    # initiate counters and binners
    top_counts = np.zeros(top_intervals)
    bottom_counts = np.zeros(bottom_intervals)
    top_bins = [round(base_g + level_width * (2 * i + 1) / 2, 5) for i in
                range(top_intervals)]
    bottom_bins = [round(base_g - level_width * (2 * i + 1) / 2, 5) for i in
                   range(bottom_intervals)]

    for n, peak, valley in signal:

        # exclude head and tail
        # if k == 0 or k == len(signal) - 1:
        #     continue

        # count peaks
        if peak >= base_g:  # if above baseline
            i = 0
            while peak >= base_g + i * level_width:
                i += 1
            top_counts[:i] += n
        else:  # if below baseline
            i = 0
            while peak <= base_g - i * level_width:
                i += 1
            bottom_counts[:i] += n

        # count valleys
        if valley >= base_g:  # if above baseline
            i = 0
            while valley >= base_g + i * level_width:
                i += 1
            top_counts[:i] += n
        else:  # if below baseline
            i = 0
            while valley <= base_g - i * level_width:
                i += 1
            bottom_counts[:i] += n

    return top_bins, bottom_bins, top_counts, bottom_counts
