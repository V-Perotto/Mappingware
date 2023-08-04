from os import path
from typing import Any, Optional
from logging import info, INFO 
from logging import debug, DEBUG
from logging import warning, WARNING
from logging import critical, CRITICAL
from logging import error, ERROR

from Settings.config import OUTPUT_LOG
from Functions.LogConfig import LogConfig


class Logger(LogConfig):
    
    def __init__(self, output: str = None) -> None:
        self.output = OUTPUT_LOG if output is None else path.join(OUTPUT_LOG, output)
    
    def debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Debug Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        debug(self.log(level=DEBUG, message=message, traceId=traceId, **kwargs))
        
    def info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Info Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        info(self.log(level=INFO, message=message, traceId=traceId, **kwargs))
        
    def warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Warning Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        warning(self.log(level=WARNING, message=message, traceId=traceId, **kwargs))
        
    def error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Error Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        error(self.log(level=ERROR, message=message, traceId=traceId, **kwargs))
        
    def critical(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Critical Level

        Args:
            message (str, optional): -> Defaults to ''.
            traceId (Optional[str], optional): -> Defaults to None.
            **kwargs (Any, optional).
        """
        critical(self.log(level=CRITICAL, message=message, traceId=traceId, **kwargs))
