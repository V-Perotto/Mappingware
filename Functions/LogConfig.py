from os import path, makedirs
from typing import Any, Optional
from datetime import datetime
from logging import basicConfig 


class LogConfig:
    
    def __init__(self):
        pass
    
    def __create_directory_if_not_exists(self, directory_path: str):
        try:
            if not path.exists(directory_path):
                makedirs(directory_path)
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

    def __create_file_log(self, filelog_per_day: bool = False) -> str:
        if filelog_per_day:
            return f"{self.output}/{datetime.now().strftime('%Y-%m-%d')}.log"
        else:
            return f"{self.output}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}.log"
        
    def __verify_file_extension(self, filename: str) -> bool:
        if '.log' in filename[-4:]:
            return f"{self.output}/{filename}"                
        return f"{self.output}/{filename}.log"
           
    def __filename(self, filename: str = None, filelog_per_day: bool = True) -> str:
        if filename == None:
            return self.__create_file_log(filelog_per_day)
        else:
            return self.__verify_file_extension(filename)
    
    def log(self, 
              level, 
              message: str = '', 
              traceId: Optional[str] = None, 
              log_format: str = f"%(asctime)s - [%(levelname)s] - %(message)s",
              filelog_per_day: bool = True,  
              **kwargs: Any) -> None:
        basicConfig(
            filename=self.__filename(filelog_per_day=filelog_per_day),
            level=level, 
            format=f"{log_format}")
        return self.__message(message, traceId=traceId, **kwargs)
        