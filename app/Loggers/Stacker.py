import os
from datetime import datetime
from Settings.config import OUTPUT_LOG
from Loggers.Logger import Logger


class Stacker():
    
    def __init__(self, output):
        self.output = os.path.join(OUTPUT_LOG, output)
        self.logger = Logger("Stacker_{output}")
    
    def __default_filename(self, filename=None) -> str:
        if filename is None:
            return f"{self.output}/{datetime.now().strftime('%Y-%m-%d')}.txt"
        return f"{self.output}/{filename}.txt"
    
    def store_string_to_txt(self, data, filename=None):
        try:
            filename = self.__default_filename(filename)
            with open(filename, 'w') as file:
                file.write(data)
            self.logger.info(message="Data has been successfully stored.", kwargs=dict(path=filename))
        except IOError:
            self.logger.error(message="Unable to write", kwargs=dict(path=filename))