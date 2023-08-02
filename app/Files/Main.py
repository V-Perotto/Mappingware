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

    def run(self):
        multiprocessing.freeze_support()
        # keylog = KeyLogger()
        # mouselog = MouseLogger()
        observer = Observer()
        logger = Logger("")
        
        if self.__is_admin():
            try:
                # keylog.keyboard_listener()
                # mouselog.mouse_listener()
                observer.activate_listeners()
            except:
                logger.error(traceback.format_exc()) 
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
