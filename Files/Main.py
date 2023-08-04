from ctypes import windll
from sys import executable, argv
from traceback import format_exc
from Settings.config import keyboard_mouse
from Loggers.Logger import Logger
from Loggers.Observer import Observer


class Main:
    
    def __init__(self):
        self.logger = Logger(keyboard_mouse)
    
    def __is_admin(self):
        try:
            return windll.shell32.IsUserAnAdmin()
        except:
            return False

    def __run_with_admin(self, observer):
        if self.__is_admin():
            try:
                observer.activate_listeners()
            except:
                self.logger.error(format_exc()) 
        else:
            # Re-run the program with admin rights
            windll.shell32.ShellExecuteW(None, "runas", executable, " ".join(argv), None, 1)
        
    def run(self, use_admin=False):
        observer = Observer()
        
        if use_admin:
            self.__run_with_admin(observer)
        else:
            observer.activate_listeners() 
        
