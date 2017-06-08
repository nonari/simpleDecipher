import logging
import sys


class Logger:

    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        progress_handler = logging.StreamHandler(sys.stdout)
        progress_handler.setLevel(logging.DEBUG)
        progress_formatter = logging.Formatter("%(message)s")
        progress_handler.setFormatter(progress_formatter)
        solutions_handler = logging.FileHandler(filename='D:/Proyectos/Python/simpledecipher/logs/temp.log')
        solutions_handler.setLevel(logging.INFO)
        solutions_formatter = logging.Formatter("%(message)s")
        progress_handler.setFormatter(solutions_formatter)
        logger.addHandler(progress_handler)
        logger.addHandler(solutions_handler)
        return logger
