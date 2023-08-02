import multiprocessing
from Loggers.KeyLogger import KeyLogger
from Loggers.MouseLogger import MouseLogger
from Loggers.Observer import Observer
from Loggers.Logger import Logger
import ctypes, sys
import traceback


class Main():
    
    def __is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def __run_with_admin(self, observer, logger):
        if self.__is_admin():
            try:
                observer.activate_listeners()
            except:
                logger.error(traceback.format_exc()) 
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        
    def run(self, use_admin=False):
        observer = Observer()
        logger = Logger("")
        
        if use_admin:
            self.__run_with_admin(observer, logger)
        else:
            observer.activate_listeners() 
        
