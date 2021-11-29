import os

dir = 'G:\\WORK ORDERS\\2021\\21028 - PAL - Beech 200 - Loads Monitoring Program\\ENGINEERING\\00_Raw_Data\\Clean - RLM\\'
file_path = dir + 'Tuesday September 28, 2021 05-23 AM - Copy.dat'

with open(file_path, 'r+', encoding="utf-8") as file:
    file.seek(0, os.SEEK_END)
    pos = file.tell() - 1

    while pos > 0 and file.read(1) != "\n":
        pos -= 1
        file.seek(pos, os.SEEK_SET)

    if pos > 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()
