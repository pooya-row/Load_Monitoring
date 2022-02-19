import os

import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns
# sns.set_theme(style='whitegrid', palette='colorblind',
#               font='DejaVu Sans', font_scale=1.3)
from utils.get_data_np import get_data
from utils.loggers import MyLog

# logger setup
logger = MyLog(console_format='%(log_color)s%(levelname)s: %(message)s').logger


def truncate_ground(input_file: str, delta: float = 1.,
                    time_diff: float = 5.) -> (int, int):
    """
    This function removes the head and tail of the data where has been
    recorded while the aircraft is grounded. The detection is based on
    changes in the W_z values when two points `time_diff` seconds apart,
    differ more than `delta`.

    :param input_file: absolute path of the raw data file
    :param delta: threshold difference
    :param time_diff: time difference between the current point and a
     point ahead (for head) or a point behind (for tail); in seconds
    :return: `head_ix` index of the character to cutoff before of;
     `tail_ix` index of the character where the bottom of the file to be
     cut off
    """

    # read data
    cols = list(range(2, 8))
    data = get_data(input_file, cols)

    # convert data into an array
    arr = np.array(data[0])
    for head_ix in range(1, len(data)):
        arr = np.c_[arr, data[head_ix]]

    # running average of the wz
    df = pd.Series(arr[:, 3])
    running_mean = df.rolling(10).mean()
    running_mean.fillna(0, inplace=True)  # fill in the blanks with zeros

    # find the head cutoff index
    head_ix = 0
    for head_ix in range(len(arr)):
        if abs(running_mean[head_ix] -
               running_mean[head_ix + time_diff * 100]) > delta:
            break
    logger.info(f'Head cutoff index is {head_ix}')

    # find the tail cutoff index
    tail_ix = len(running_mean)
    for tail_ix in range(len(running_mean) - 1, -1, -1):
        if abs(running_mean[tail_ix] -
               running_mean[tail_ix - 100 * time_diff]) > delta:
            break
    logger.info(f'Tail cutoff index is {tail_ix}')

    return head_ix, tail_ix
    # return arr[head_ix:tail_ix, [0, 3, 6]], \
    #        [data[k] for k in [0, 3, 6]], running_mean


if __name__ == '__main__':
    # source directory - only the desired files must be here, nothing else
    # src_address = input('Where are the source files: ')
    src_address = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\to trim\\'

    # destination directory - can be anywhere
    # dst_address = input('Where should I store the trimmed files: ')
    dst_address = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\trimmed\\'

    # generate a list of all source files
    files_list = os.listdir(src_address)

    for f in files_list:  # loop through all source flies
        origin = src_address + f
        target = dst_address + f[:-4] + '_trimmed.dat'

        # determine cutoff limits
        logger.info(f'Determining cutoff indices for "{f}"')
        head_cutoff, tail_cutoff = truncate_ground(origin, .8, 5.)

        # write to a new file line by line
        logger.info(f'Writing trimmed data to "{f[:-4] + "_trimmed.dat"}"\n')
        with open(origin, 'r') as raw:
            raw.seek(head_cutoff * 153, os.SEEK_SET)
            with open(target, 'w') as trimmed:
                while raw.tell() < tail_cutoff * 153:
                    trimmed.write(raw.readline())

    # plot stuff!
    # fig, ax = plt.subplots(2, 1, sharex='col')
    # # wz - original data
    # ax[0].plot(original_data[0], original_data[1],
    #            label=r'$\omega_Z$ original', linewidth=.5)
    # # wz - trimmed data
    # ax[0].plot(truncated_data[:, 0], truncated_data[:, 1],
    #            label=r'$\omega_Z$ truncated', linewidth=.5)
    # # wz - running average
    # ax[0].plot(original_data[0], ra,
    #            label=r'$\omega_Z$ running avg', linewidth=.5)
    # ax[0].legend(loc=2, fontsize=15)
    #
    # # Nz - original data
    # ax[1].plot(original_data[0], original_data[2],
    #            label=r'$N_Z$ original', linewidth=.5)
    # # Nz - trimmed data
    # ax[1].plot(truncated_data[:, 0], truncated_data[:, 2],
    #            label=r'$N_Z$ truncated', linewidth=.5)
    # ax[1].legend(loc=2, fontsize=15)
    # plt.show()
