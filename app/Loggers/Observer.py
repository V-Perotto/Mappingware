from multiprocessing import Process
from threading import Thread

from Loggers.KeyLogger import KeyLogger
from Loggers.MouseLogger import MouseLogger

class Observer():
    
    def activate_listeners(self):        
        thread_mouse = Thread(target=MouseLogger().mouse_listener)
        thread_key = Thread(target=KeyLogger().keyboard_listener)
        
        thread_mouse.start()
        thread_key.start()
        
        thread_mouse.join()
        thread_key.join()
        