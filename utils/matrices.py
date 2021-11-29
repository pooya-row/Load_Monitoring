import numpy as np

from utils import material_lib
from math import floor, ceil


def mean_range_matrix(cycles, mean_bin_size, range_bin_size):
    """
    Generates the mean-range matrix based on the input ``cycles`` matrix
    and mean and range bin sizes.

    Parameters
    ----------
    cycles: np.ndarray
        matrix formed after cycle extraction.
    mean_bin_size: float
        The bin size used to divide the ``mean`` values.
    range_bin_size: float
        The bin size used to divide the ``range`` values.

    Returns
    -------
    m_r_matrix : np.ndarray
        The mean-range matrix.
    """

    global m_r_matrix, mean_bin_edges, range_bin_edges

    mean_bin_edges = np.arange(np.floor(np.amin(cycles[:, 0])),
                               np.ceil(np.amax(cycles[:, 0])) + mean_bin_size,
                               mean_bin_size)
    range_bin_edges = np.arange(np.floor(np.amin(cycles[:, 1])),
                                np.ceil(
                                    np.amax(cycles[:, 1])) + range_bin_size,
                                range_bin_size)

    m_r_matrix = np.zeros((len(range_bin_edges) - 1, len(mean_bin_edges) - 1))
    m = np.digitize(cycles[:, 0], mean_bin_edges, right=True) - 1
    r = np.digitize(cycles[:, 1], range_bin_edges, right=True) - 1

    for i in range(len(cycles)):
        m_r_matrix[r[i], m[i]] += cycles[i, 2]

    return m_r_matrix


def from_to(cycles, from_bin_size, to_bin_size):
    """
    Generates the From-To matrix based on the input ``cycles`` matrix and
    **from** and **to** bin sizes.

    Parameters
    ----------
    cycles: np.ndarray,
        matrix formed after cycle extraction.

    from_bin_size: float
        The bin size used to divide the ``from`` values.

    to_bin_size: float
        The bin size used to divide the ``to`` values.

    Returns
    -------
    from_to_matrix: np.ndarray
        The from-to matrix.
    """

    from_bin_edges = np.arange(np.floor(np.amin(cycles[:, 3])),
                               np.ceil(np.amax(cycles[:, 3])) + from_bin_size,
                               from_bin_size)
    to_bin_edges = np.arange(np.floor(np.amin(cycles[:, 4])),
                             np.ceil(np.amax(cycles[:, 4])) + to_bin_size,
                             to_bin_size)

    from_to_matrix = np.zeros((len(to_bin_edges) - 1, len(from_bin_edges) - 1))
    t = np.digitize(cycles[:, 4], to_bin_edges, right=True) - 1
    f = np.digitize(cycles[:, 3], from_bin_edges, right=True) - 1
    for i in range(len(cycles)):
        from_to_matrix[t[i], f[i]] += cycles[i, 2]

    return from_to_matrix


def damage(material, k_t):
    """
    Determines a matrix the same shape as the mean-range matrix,
    the elements of which are the number of cycles-to-failure for a given
    material and the corresponding cycle type from mean-range matrix.
    Dividing the mean-range matrix to this one, damage due to each type of
    cycles are determined and then summed based on Minor rule.

    Important Note
    ----------
    This function must be called after the ``mean_range_matrix`` because
    ``m_r_matrix``, ``mean_bin_edges`` and ``range_bin_edges`` are global
    parameters which are defined in that function.

    Parameters
    ----------
    material: str
        Name of the material, must exist in the material library.
    k_t: str
        The kₜ corresponding to a particular form of the selected material
        above.

    Returns
    -------
    damage: float
        The total damage.
    """

    mean_bins = np.array(
        [(i + j) / 2 for i, j in zip(mean_bin_edges[1:], mean_bin_edges[:-1])])
    range_bins = np.array([(i + j) / 2 for i, j in
                           zip(range_bin_edges[1:], range_bin_edges[:-1])])
    N_matrix = np.zeros(m_r_matrix.shape)
    a, b, c, d = material_lib.property_selector(material, k_t)

    for i in range(N_matrix.shape[0]):
        for j in range(N_matrix.shape[1]):
            # TODO: the 200 factor is for generating positive argument in
            #  the log function while acceleration signal is used instead
            #  of the stress values. Should be removed when proper stress
            #  calculation is done properly.
            s_max = (mean_bins[j] + range_bins[i] / 2) * 200
            s_min = (mean_bins[j] - range_bins[i] / 2) * 200

            try:
                r = s_min / s_max
            except ValueError:
                r = 0.

            try:
                s_eq = s_max * (1 - r) ** d
            except ValueError:
                r = 0.
                s_eq = s_max * (1 - r) ** d

            # TODO: the sign in the log argument must be negative log(s_eq - c)
            N_matrix[i, j] = 10 ** (a - b * np.log(s_eq - c))

    # ==================== damage ====================
    damage_matrix = m_r_matrix / N_matrix
    return damage_matrix.sum()


def level_cross_count(signal: np.ndarray,
                      level_width: float,
                      base_g: float = 1.) -> (
        list, list, np.ndarray, np.ndarray):
    """
    Counts the level crossing given a baseline, resolution, and an ``(n ×
    3)`` array containing counts, max and min of each cycle type. This
    array is the last three columns of the array generated by the
    ``rainflow.extract_cycles`` function.

    Parameters
    ---------
    signal:
        ``(n × 3)`` array. Each row represents a type of cycle. First
        column is the counts of that cycle type, resulted from rainflow
        counting. Second column is the maximum value of that cycle family
        and the third column is the minimum value of that cycle family.

    level_width:
        Width of the desired levels.

    base_g:
        Baseline.

    Returns
    --------
    tuple[list[float], list[float], ndarray, ndarray]
        two lists containing the bins above and below baseline, and two
        arrays containing the counts of each bin above and below baseline.
    """

    # largest and smallest signals
    max_signal = max(signal[:, 1])
    min_signal = min(signal[:, 2])

    if (max_signal - base_g) % level_width != 0.0:  # intervals above baseline
        top_intervals = ceil((max_signal - base_g) / level_width)
    else:  # reversal exactly on a bin border
        top_intervals = ceil((max_signal - base_g) / level_width) + 1

    if (min_signal - base_g) % level_width != 0.0:  # intervals below baseline
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
