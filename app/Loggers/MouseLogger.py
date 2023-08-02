import time
from pynput.mouse import Listener
from Loggers.Logger import Logger

logger = Logger("Mouse")

class MouseLogger(Logger):
    
    def __init__(self) -> None:
        self.clicks = []
    
    def set_clicks(self, click) -> None:
        self.clicks.append(click)
        
    def get_clicks(self) -> list:
        return self.clicks
        
    def on_click(self, button_name) -> None:
        timestamp = time.time()
        self.clicks.append((timestamp, button_name))
        
    def get_clicks(self) -> list:
        return self.clicks
    
    def on_move(self, x, y) -> None:
        logger.info(message="Mouse moved to ({0}, {1})".format(x, y))

    def on_click(self, x, y, button, pressed) -> None:
        if pressed:
            logger.info(message='Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

    def on_scroll(self, x, y, dx, dy) -> None:
        logger.info(message='Mouse scrolled at ({0}, {1}) ({2}, {3})'.format(x, y, dx, dy))

    def mouse_listener(self) -> None:
        with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            lister = listener.join()
            logger.debug(lister)
        listener.stop()