from pynput.mouse import Listener
from Loggers.Logger import Logger
from Loggers.Stacker import Stacker
import time

mouse = "Mouse"

logger = Logger(mouse)
stacker = Stacker(mouse)

class MouseLogger():
    
    def __init__(self) -> None:
        self.clicks = []        
    
    def __on_move(self, x, y) -> None:
        
        logger.info(message="Mouse moved to ({0}, {1})".format(x, y))

    def __on_click(self, x, y, button, pressed) -> None:
        if pressed:
            
            logger.info(message='Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

    def __on_scroll(self, x, y, dx, dy) -> None:
        
        logger.info(message='Mouse scrolled at ({0}, {1}) ({2}, {3})'.format(x, y, dx, dy))

    def mouse_listener(self) -> None:
        with Listener(on_move=self.__on_move, on_click=self.__on_click, on_scroll=self.__on_scroll) as listener:
            listener.join()