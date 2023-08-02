import os
from typing import Any, Optional
from datetime import datetime
import logging
from Settings.config import OUTPUT_LOG

class Logger():
    
    def __init__(self, output: str = None) -> None:
        self.output = OUTPUT_LOG if output is None else os.path.join(OUTPUT_LOG, output)
    
    def __create_directory_if_not_exists(self, directory_path: str):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
        except OSError as e:
            raise f"Error: {e}"
    
    def __add_kwargs_in_log(self, kwargs, args = "") -> str:
        count = 0
        for key, value in kwargs.items():
            count += 1
            if len(kwargs.items()) > 1:
                args += f"{key}={value} | " if count < len(kwargs.items()) else f"{key}={value}"
            else:
                args += f"{key}={value}"
        return args
        
    def __message(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = message
        if traceId:
            msg = f"ID: {traceId} | {message}"
        
        args = self.__add_kwargs_in_log(kwargs)
        if args == "":
            msg = args if message == '' else f'{msg}'
        else:
            msg = args if message == '' else f'{msg} | {args}'
        return msg

    def __create_file_log(self, datetime_now, filelog_per_day: bool = False) -> str:
        if filelog_per_day:
            return f"{self.output}/{datetime_now.strftime('%Y-%m-%d')}.log"
        else:
            return f"{self.output}/{datetime_now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.log"
        
    def __verify_file_extension(self, filename: str) -> bool:
        if '.log' in filename[-4:]:
            return f"{self.output}/{filename}"                
        return f"{self.output}/{filename}.log"
           
    def __filename(self, filename: str = None, filelog_per_day: bool = True) -> str:
        if filename == None:
            return self.__create_file_log(datetime.now(), filelog_per_day)
        else:
            return self.__verify_file_extension(filename)
    
    def __log(self, 
              level, 
              message: str = '', 
              traceId: Optional[str] = None, 
              log_format: str = f"%(asctime)s - [%(levelname)s] - %(message)s",
              filelog_per_day: bool = True,  
              **kwargs: Any) -> None:
        logging.basicConfig(
            filename=self.__create_directory_if_not_exists(
                self.__filename(filelog_per_day=filelog_per_day)
                ), 
            level=level, 
            format=f"{log_format}")
        msg = self.__message(message, traceId=traceId, **kwargs)
        return msg
    
    def debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Debug Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        logging.debug(self.__log(level=logging.DEBUG, message=message, traceId=traceId, **kwargs))
        
    def info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Info Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        logging.info(self.__log(level=logging.INFO, message=message, traceId=traceId, **kwargs))
        
    def warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Warning Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        logging.warning(self.__log(level=logging.WARNING, message=message, traceId=traceId, **kwargs))
        
    def error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Error Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        logging.error(self.__log(level=logging.ERROR, message=message, traceId=traceId, **kwargs))
        
    def critical(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Critical Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        logging.critical(self.__log(level=logging.CRITICAL, message=message, traceId=traceId, **kwargs))
