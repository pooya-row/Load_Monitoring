import logging
from colorlog import ColoredFormatter


class MyLog:
    def __init__(self,
                 console_format='''
                 %(log_color)s%(levelname)s [%(asctime)s] %(message)s%(reset)s
                 ''',
                 log_file=None,
                 file_format='%(levelname)s [%(asctime)s] %(message)s'):
        self.logger = logging.getLogger(__name__)  # create logger
        self.logger.setLevel(logging.INFO)  # set logger's leve

        # create formatter
        formatter = ColoredFormatter(console_format)
        # create stream handler
        console_handler = logging.StreamHandler()
        # assign formatter to stream handler
        console_handler.setFormatter(formatter)
        # assign console handler to logger
        self.logger.addHandler(console_handler)

        # create file handler
        if log_file is not None:
            formatter = logging.Formatter(file_format)
            file_handler = logging.FileHandler(log_file, 'w')
            # assign formatter to file handler
            file_handler.setFormatter(formatter)
            # assign log file handler to logger
            self.logger.addHandler(file_handler)
