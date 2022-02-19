"""
This script re-formats the raw data into a NASGRO-friendly input type.

`rearrange_raw` function rearranges the Nz into two columns to be considered
peaks and valleys.

`rearrange_p_v` on the other hand, extracts the peaks
and valleys first and then puts the peaks in the first columns and the
valleys in the second. NASGRO likes to see a third column which indicates
the number of repetitions of peaks and valleys, which is 1 in our case
since we are using random data.
"""
import logging

import fatpack
import numpy as np
from colorlog import ColoredFormatter
from matplotlib import pyplot as plt

from utils.get_data_np import get_data

# logger setup
logger = logging.getLogger(__name__)  # create logger
logger.setLevel(logging.INFO)  # set logger's leve

# create formatter
formatter = ColoredFormatter('%(log_color)s%(levelname)s [%(asctime)s] '
                             '%(message)s%(reset)s')

console_handler = logging.StreamHandler()  # create stream handler
console_handler.setFormatter(formatter)  # assign formatter to stream handler

logger.addHandler(console_handler)  # assign handler to logger


def rearrange_raw(input_file: str, output_file: str):
    t, nz = get_data(input_file, [7])

    # if odd number of lines, remove the last
    if len(nz) % 2 == 1:
        nz = nz[:-1]
        t = t[:-1]

    # reformat signal into two columns
    nz_re = nz.reshape((len(nz) // 2, -1)).copy()

    # add counts column to the end (all 1s)
    nz_re = np.c_[nz_re, np.ones(len(nz_re))]

    # write into file
    with open(output_file, 'w') as new:
        for line in nz_re:
            new.write(f'{line[0]:.7f} {line[1]:.7f} {int(line[2])}\n')

    return t, nz


def rearrange_p_v(input_file: str, output_file1: str, output_file2: str):
    """
    Extract peaks and valleys (reversals) and then reformat Nz into two
    columns.

    :param input_file: The path to the input raw data
    :param output_file1: The path to the new file ordered as peaks and valleys
    :param output_file2: The path to the new file ordered as valleys and peaks
    :return: time and reversals for plot
    """
    t, nz = get_data(input_file, [7])
    nz = np.array(nz).reshape(-1)
    reversals, ix = fatpack.find_reversals(nz, k=512)

    # if odd number of lines, remove the last
    if len(reversals) % 2 == 1:
        reversals = reversals[:-1]
        ix = ix[:-1]

    # reformat reversals into two columns
    reversals_re = reversals.reshape((len(reversals) // 2, -1)).copy()

    # swap the first two columns if the first one is the valleys
    if reversals_re[0, 0] < reversals_re[0, 1]:
        reversals_re[:, [1, 0]] = reversals_re[:, [0, 1]]

    # add reversal count column to the end (all 1s)
    reversals_re = np.c_[reversals_re, np.ones(len(reversals_re))]

    # write peaks and valleys file
    with open(output_file1, 'w') as new:
        new.write(f'peak      valley    reps\n')
        last_valley = -999.

        for line in reversals_re:
            # if last valley is equal or larger than the current peak, skip
            if line[0] > last_valley:
                new.write(f'{line[0]:.7f} {line[1]:.7f} {int(line[2])}\n')
                last_valley = line[1]
            else:
                continue

            # if peak is smaller or equal to valley, report
            if line[0] <= line[1]:
                logger.warning(f'{line} is invalid.')

    # generate valleys and peaks file
    reversals_re[:, [1, 0]] = reversals_re[:, [0, 1]]
    with open(output_file2, 'w') as new:
        new.write(f'peak      valley    reps\n')
        last_valley = -999.

        for line in reversals_re:
            if line[1] > last_valley:
                new.write(f'{line[0]:.7f} {line[1]:.7f} {int(line[2])}\n')
                last_valley = line[0]
            else:
                continue

    return t[ix], reversals


if __name__ == '__main__':
    d1 = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\test run\\'
    d2 = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\data for NASGRO\\'
    files = ['Friday December 10, 2021 06-08 AM',
             'Monday November 15, 2021 01-04 PM',
             'Tuesday September 14, 2021 12-39 PM_TimeAdded']

    for f in files:
        # to, n_z = rearrange_raw(d1 + f + '.dat', d2 + f + '_refmt.dat')
        logger.info(f'"{f}" is being processed.')

        t_rev, rev_re = rearrange_p_v(d1 + f + '.dat',
                                      d2 + f + '_refmt_fltred.dat',
                                      d2 + f + '_refmt_fltred_rev.dat')

        logger.info(f'"{f}" was successfully processed.\n')

    # plt.plot(to, n_z, label='original', linewidth=0.5)
    # plt.plot(t_rev, rev_re, label='filtered', linewidth=0.5)
    # plt.legend(fontsize=15)
    # plt.grid(True, linewidth=0.3, alpha=0.5)
    # plt.show()
