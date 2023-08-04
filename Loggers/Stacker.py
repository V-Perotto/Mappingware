from os import path
from datetime import datetime
from Settings.config import OUTPUT_LOG


class Stacker:
    
    def __init__(self):
        self.output = path.join(OUTPUT_LOG, "Stacker")
    
    def __default_filename(self, filename=None) -> str:
        if filename is None:
            return f"{self.output}/{datetime.now().strftime('%Y-%m-%d')}.txt"
        return f"{self.output}/{filename}.txt"
    
    def store_string_to_txt(self, data, filename=None):
        try:
            filename = self.__default_filename(filename)
            with open(filename, 'a') as file:
                file.write(data)
        except IOError:
            raise IOError