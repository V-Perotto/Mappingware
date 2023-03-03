import os
import logging
from datetime import datetime
from pathlib import Path, PurePath
from Loggers.Logger import Logger

ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

OUTPUT_LOG = "Output/Logs"

log_path = Path(PurePath(ROOT, OUTPUT_LOG))

default_log_msg = "[{ticket_id}] - [{prestador}] - [{nr}] {msg}"
out_robot_log_level = logging.INFO
out_robot_file_log_level = logging.INFO
out_robot_logger_name = 'robot-logger-name'
out_robot_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"
if not log_path.is_dir():
    log_path.mkdir(parents=True, exist_ok=True)

def create_file_log(datetime_now):
    return f"{OUTPUT_LOG}/{datetime_now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.log"

def get_file_handler():
    now = datetime.now()
    file_handler = logging.FileHandler(create_file_log(now), encoding='utf-8')
    file_handler.setLevel(out_robot_log_level)
    file_handler.setFormatter(logging.Formatter(out_robot_log_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(out_robot_log_level)
    stream_handler.setFormatter(logging.Formatter(out_robot_log_format))
    return stream_handler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(out_robot_log_level)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger

# logger = get_logger('teste')
# print(logger)
Logger().log_info(message='info level') #, traceId="JOBS", teste='newtest', addmore="things")
# Logger().log_warn(message="warning level")
# Logger().log_debug(message="debug level")
# Logger().log_error(message="error level")
# Logger().log_critical(message="critical level")