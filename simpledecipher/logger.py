import logging

import sys


class Logger:

    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger