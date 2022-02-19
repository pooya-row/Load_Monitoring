import logging
import os

import numpy as np
import pandas as pd
from colorlog import ColoredFormatter

from utils.get_data_np import get_data

# logger setup
from utils.loggers import MyLog

logger = MyLog('%(log_color)s%(levelname)s: %(message)s').logger


def truncate_last_line(f: str):
    """
    This function truncates the end of raw data files where there is an
    incomplete line.

    :param f: absolute path to the input raw file
    :return: None
    """
    with open(f, 'r+') as file:
        file.seek(0, os.SEEK_END)  # go to last byte of the file
        ll = file.tell()
        print(f'll = {ll}')
        file.seek(file.tell() - 154, os.SEEK_SET)  # go 154 chars back
        temp_str = file.read(2)  # read 2 chars from there

        if '\n' in temp_str:
            pass
        else:
            file.seek(0, os.SEEK_END)
            pos = file.tell()
            while file.read(1) != '\n':
                pos -= 1
                file.seek(pos, os.SEEK_SET)

            file.seek(pos, os.SEEK_SET)
            file.truncate()


def truncate_ground(input_file: str, delta: float = 1., time_diff: float = 5.):
    """
    This function removes the head and tail of the data where has been
    recorded while the aircraft is grounded. The detection is based on
    changes in the W_z values when two points `time_diff` seconds apart,
    differ more than `delta`.

    :param input_file: absolute path of the raw data file
    :param delta: threshold difference
    :param time_diff: time difference between the current point and a
     point ahead (for head) or a point behind (for tail); in seconds
    :return: trimmed array containing time, wz, Nz; original data containing
     time, wz, Nz; running average array of wz
    """
    # read data
    cols = list(range(2, 8))
    data = get_data(input_file, cols)

    # convert data into an array
    arr = np.array(data[0])
    for i in range(1, len(data)):
        arr = np.c_[arr, data[i]]

    # running average of the wz
    df = pd.Series(arr[:, 3])
    running_mean = df.rolling(10).mean()
    running_mean.fillna(0, inplace=True)  # pad the running average with zeros

    # find the head cutoff index
    i = 0
    for i in range(len(arr)):
        if abs(running_mean[i] - running_mean[i + time_diff * 100]) > delta:
            break
    logger.info(f'Head cutoff index is {i}')

    # find the tail cutoff index
    j = len(running_mean)
    for j in range(len(running_mean) - 1, -1, -1):
        if abs(running_mean[j] - running_mean[j - 100 * time_diff]) > delta:
            break
    logger.info(f'Tail cutoff index is {j}')

    return arr[i:j, [0, 3, 6]], [data[k] for k in [0, 3, 6]], running_mean


if __name__ == '__main__':
    file_address = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\to ' \
                   'salvage\\tt\\00-Wednesday September 15, 2021 05-51 ' \
                   'AM_TimeAdded.dat'
    truncate_last_line(file_address)
