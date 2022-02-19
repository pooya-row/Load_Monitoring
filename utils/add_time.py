import datetime
import logging
import os

from utils.loggers import MyLog


def truncate_end(fl):
    """
    Removes the last incomplete line from IMU file.

    :param fl: input file which must have writing permissions.
    :return: None
    """
    # go to end and track back a 154-char line. If it doesn't land on an
    # end-of-line char, trace the last EOL char and truncate from there
    fl.seek(0, os.SEEK_END)  # go to last byte of the file
    ll = fl.tell()
    fl.seek(ll - 154, os.SEEK_SET)  # go 154 chars back
    temp_str = fl.read(2)  # read 2 chars from there

    if '\n' in temp_str:
        pass
    else:
        fl.seek(0, os.SEEK_END)
        pos = fl.tell() - 2
        ts = fl.read(1)
        while ts != '\n':
            pos -= 1
            fl.seek(pos, os.SEEK_SET)
            ts = fl.read(1)

        fl.seek(pos, os.SEEK_SET)
        fl.truncate()


# logger
logger = MyLog(console_format='%(levelname)s [%(asctime)s] %(message)s',
               log_file='change.log'
               ).logger

# source directory - only the desired files must be here, nothing else
src_address = input('Where are the source files: ')
# src_address = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\to salvage'

# destination directory - can be anywhere
dst_address = input('Where should I store the reformatted files: ')
# dst_address = 'C:\\Users\\pooya.rowghanian\\Desktop\\New folder\\salvaged'

# generate a list of all source files
files_list = os.listdir(src_address)

for f in files_list:  # loop through all source flies
    t_str = '01-06-1980 00:00:00.000000'  # start time
    t = datetime.datetime.strptime(t_str, '%d-%m-%Y %H:%M:%S.%f')

    old_file = os.path.join(src_address, f)  # full address of source file

    ext = os.path.splitext(f)[1]
    if ext != '.dat':  # only use *.dat files
        pass
    else:
        # full address of edited file
        new_file = os.path.join(dst_address, os.path.splitext(f)[0] +
                                '_TimeAdded.dat')
        logger.info(f'Opening\t\t{f}')
        with open(old_file, 'r') as src:  # open source file

            if len(src.readline()) == 152:  # check first line length
                logger.info(f'___Not changed___ {f}\n')
            else:
                logger.info(f'Processing\t{f}')
                with open(new_file, 'w+') as dst:  # open new file
                    for line in src:  # loop over each line of source file
                        t += datetime.timedelta(milliseconds=10)  # add 10ms

                        # write the line to new file:
                        #   1. format and write timestamp
                        #   2. write a zero & 2 spaces at the end of timestamp
                        #   3. remove last 20 characters & write the remainder
                        #   4. write a space, a 4 and a line break to the end
                        dst.write('%s0  %s 4\n' % (
                            datetime.datetime.strftime(t,
                                                       '%d-%m-%Y %H:%M:%S.%f'),
                            line.rstrip('\n')[:-20]))

                    # remove the incomplete trailing line
                    truncate_end(dst)
                    logger.info(f'Truncated {f}')

                logger.info(f'=== Completed === {f}\n')
