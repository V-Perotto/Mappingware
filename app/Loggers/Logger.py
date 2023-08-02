import os
from typing import Any, Optional
from datetime import datetime
import logging
from Settings.config import OUTPUT_LOG

output_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"

class Logger():
    
    def __init__(self, output) -> None:
        self.output = os.path.join(OUTPUT_LOG, output)
    
    def __add_kwargs_in_log(self, kwargs, args = "") -> str:
        count = 0
        for key, value in kwargs.items():
            count += 1
            if len(kwargs.items()) > 1:
                args += f"{key}={value} | " if count < len(kwargs.items()) else f"{key}={value}"
            else:
                args += f"{key}={value}"
        return args
        
    def _message(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = message
        if traceId:
            msg = f"ID: {traceId} | {message}"
        
        args = self.__add_kwargs_in_log(kwargs)
        if args == "":
            msg = args if message == '' else f'{msg}'
        else:
            msg = args if message == '' else f'{msg} | {args}'
        return msg

    def _create_file_log(self, datetime_now, log_per_day: bool = False) -> str:
        if log_per_day:
            # cria um arquivo de log por dia
            return f"{self.output}/{datetime_now.strftime('%Y-%m-%d')}.log"
        else:
            # cria um arquivo de log por mensagem de log
            return f"{self.output}/{datetime_now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.log"
        
    def __verify_file_extension(self, filename: str) -> bool:
        if '.log' in filename[-4:]:
            return f"{self.output}/{filename}"                
        return f"{self.output}/{filename}.log"
           
    def _filename(self, filename: str = None, log_per_day: bool = True) -> str:
        if filename == None:
            return self._create_file_log(datetime.now(), log_per_day)
        else:
            return self.__verify_file_extension(filename)
    
    def __log(self, 
              level, 
              message: str = '', 
              traceId: Optional[str] = None, 
              log_format: str = output_log_format,
              log_per_day: bool = True,  
              **kwargs: Any) -> None:
        logging.basicConfig(filename=self._filename(log_per_day=log_per_day), level=level, format=f"{log_format}")
        msg = self._message(message, traceId=traceId, **kwargs)
        return msg
    
    def debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.debug(self.__log(level=logging.DEBUG, message=message, traceId=traceId, **kwargs))
        
    def info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.info(self.__log(level=logging.INFO, message=message, traceId=traceId, **kwargs))
        
    def warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.warning(self.__log(level=logging.WARNING, message=message, traceId=traceId, **kwargs))
        
    def error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.error(self.__log(level=logging.ERROR, message=message, traceId=traceId, **kwargs))
        
    def critical(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.critical(self.__log(level=logging.CRITICAL, message=message, traceId=traceId, **kwargs))
