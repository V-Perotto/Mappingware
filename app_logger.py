import logging
from datetime import datetime
from variables import config


def get_file_handler():
    now = datetime.now()
    file_handler = logging.FileHandler(
        f"Results/{now.strftime('%Y%m%d%H%M%S%f')}.log",
        encoding='utf-8')
    file_handler.setLevel(config.out_robot_log_level)
    file_handler.setFormatter(logging.Formatter(config.out_robot_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(config.out_robot_log_level)
    stream_handler.setFormatter(logging.Formatter(config.out_robot_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(config.out_robot_log_level)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
