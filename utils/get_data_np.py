import gc
import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

import numpy as np

logger = logging.getLogger(__name__)  # create logger
logger.setLevel(logging.INFO)  # set logger's leve

# formatter = logging.Formatter('[%(name)s %(asctime)s]: %(message)s')  # create
# formatter
formatter = ColoredFormatter('%(log_color)s[%(levelname)s: %(asctime)s issued'
                             ' from %(name)s]: \n\t%(message)s%(reset)s')

console_handler = logging.StreamHandler()  # create stream handler
console_handler.setFormatter(formatter)  # assign formatter to stream handler

logger.addHandler(console_handler)  # assign handler to logger


def get_data(file_path: str,
             col_list: list) -> list:
    """
    Reads data file generated by "IMU" and parses the desired columns.


    Note
    -------
    This function first checks whether the last line of the IMU file misses
    dara in which case removes the line permanently.


    Parameters
    -------
    file_path : str
        The path to the `dat` file containing timestamp and acceleration
        components.

    col_list : list
        The list of desired columns to be extracted excluding the datetime
        column. Datetime column is always included as the first column.


    Returns
    -------
    list
        a list of 1D arrays. First item is datetime column, the rest are
        defined by ``col_list``.
    """

    use_cols = [0, 1] + col_list

    # check if the last line has any missing data. remove line if so
    with open(file_path, 'r+') as file:

        file.seek(0, os.SEEK_END)  # go to last byte of the file
        last_pos = file.tell()  # record the position of the last byte
        pos = file.tell() - 1

        file.seek(pos, os.SEEK_SET)  # go one position back
        temp_str = file.read(1)  # read from current position

        # Beginning of an empty line at the EOF
        if temp_str == '\n' and last_pos % 153 in [0, 152]:
            pass

        # at the end of a complete line
        elif temp_str != '\n' and last_pos % 153 == 151:
            pass

        else:
            while file.read(1) != "\n":  # find EOL of the last complete line
                pos -= 1
                file.seek(pos, os.SEEK_SET)

            file.seek(pos, os.SEEK_SET)  # go there
            file.truncate()  # truncate from current position
            logger.warning(f'The Last line of the IMU file "{file.name}"'
                           f' was deleted due to incomplete data record.')
            # print(f'\nWARNING: Last line of the IMU file "{file.name}" was '
            #       f'deleted due to incomplete data record.\n')

        data = np.loadtxt(file.name, dtype='object', usecols=use_cols)

    # convert the first two columns into a column of seconds
    data[:, 0] = data[:, 0] + [' '] + data[:, 1]
    data = np.delete(data, 1, 1)
    data[:, 1:] = data[:, 1:].astype('float64')

    t0 = datetime.strptime(data[0, 0][:-1], '%d-%m-%Y %H:%M:%S.%f')

    data[:, 0] = [
        (datetime.strptime(x[:-1],
                           '%d-%m-%Y %H:%M:%S.%f') - t0).total_seconds()
        for x in data[:, 0]]

    gc.collect()

    return [data[:, i].reshape((-1, 1)) for i in range(data.shape[1])]
