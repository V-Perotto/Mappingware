import os
import json
import traceback
from datetime import datetime
from Loggers.app_logger import ROOT
from Loggers.Logger import Logger

OUTPUT_JSON = r"Output/Json" 

class JSONLib():

    def __init__(self) -> None:
        self.input_path = OUTPUT_JSON
        self.output_path = OUTPUT_JSON
        
    def _create_file_json(self, datetime_now, log_per_day: bool = True) -> str:
        if log_per_day:
            # cria um arquivo de log por dia
            return f"{datetime_now.strftime('%Y-%m-%d')}.json"
        else:
            # cria um arquivo de log por mensagem de log
            return f"{datetime_now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.json"
        
    def __validate_json_name(self, filename: str) -> str:
        if not '.json' in filename[-5:]:
            filename = f"{filename}.json"
        return filename

    def __read(self, filename: str, json_file_path: str = None):
        """Read a .json file. \n
            - OPTIONAL = Default path is from Input directory.
        """
        if json_file_path is None:
            json_file_path = self.input_path
        try:
            with open(os.path.join(json_file_path, self.__validate_json_name(filename)), "r") as openfile:
                json_obj = json.load(openfile)
            return json_obj
        except Exception as e:
            raise e     # f'Error to read a JSON file. \n{e}' 

    def __write(self, filename: str, dict_package: dict, json_file_path: str = None):
        """Write a .json file. \n
            - OPTIONAL = Default path is from Output directory. 
        """
        if json_file_path is None:
            json_file_path = self.output_path
        try:
            with open(os.path.join(json_file_path, self.__validate_json_name(filename)), "a") as outfile:
                json.dump(dict_package, outfile)       
            return True
        except:       
            raise Exception(f'Error to write a JSON file.\n{traceback.format_exc()}')
        
    def read_json(self, filename: str = None, json_file_path: str = None) -> None:
        if filename is None and json_file_path is None:
            self.__read(self._create_file_json(datetime.now(), OUTPUT_JSON), OUTPUT_JSON)
        else:
            self.__read(filename, json_file_path)
        
    def write_json(self, dict_package: dict, filename: str = None, json_file_path: str = None) -> None:
        if filename is None and json_file_path is None:
            self.__write(self._create_file_json(datetime.now(), OUTPUT_JSON), dict_package, OUTPUT_JSON)
        else:
            self.__write(filename, dict_package, json_file_path)
            
    def save_text_data(self, text: str, cmd_pressed: str) -> None:        
        try:
            logger = Logger()
            
            FULL_PATH = os.path.join(ROOT, OUTPUT_JSON)
            
            filename = os.path.join(FULL_PATH, 
                                    self.__validate_json_name(
                                        self._create_file_json(
                                            datetime.now(), 
                                            OUTPUT_JSON)
                                        )
                                    )
            json_list = []
            
            if os.path.isfile(filename) is False:
                file_json = open(filename)
                file_json.close()
            
            # Read JSON file
            with open(filename, 'r') as fp:
                json_list = json.load(fp)
            
            json_list.append({
                "text": text,
                "cmd_press": cmd_pressed            
            })
            
            with open(filename, 'w') as json_file:
                json.dump(json_list, json_file, indent=4, separators=(',',': '))
        
        except Exception:
            return Exception("Error to create, save, or modify json file.")