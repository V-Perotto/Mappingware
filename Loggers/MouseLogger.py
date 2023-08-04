from pynput.mouse import Listener
from Loggers.Logger import Logger
from Settings.config import keyboard_mouse
from Settings.initializer import stacker


class MouseLogger:
        
    def __init__(self) -> None:
        self.logger = Logger(keyboard_mouse)    
    
    def __on_move(self, x, y) -> None:
        stacker.store_string_to_txt(f"({str(x)}, {str(y)})\n")
        self.logger.info(message="Mouse moved to ({0}, {1})".format(x, y))

    def __on_click(self, x, y, button, pressed) -> None:
        if pressed:
            stacker.store_string_to_txt(f"({str(x)}, {str(y)}), {str(button)}\n")
            self.logger.info(message='Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

    def __on_scroll(self, x, y, dx, dy) -> None:
        stacker.store_string_to_txt(f"({str(x)}, {str(y)}), ({str(dx)}, {str(dy)})\n")
        self.logger.info(message='Mouse scrolled at ({0}, {1}) ({2}, {3})'.format(x, y, dx, dy))

    def mouse_listener(self) -> None:
        with Listener(on_move=self.__on_move, on_click=self.__on_click, on_scroll=self.__on_scroll) as listener:
            listener.join()