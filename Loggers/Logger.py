import os
from typing import Any, Optional
from datetime import datetime
import pytz
import logging
# from elasticsearch import Elasticsearch

ROBOT_NAME = os.environ.get("ROBOT_NAME","roboname")
CLIENT = os.environ.get("CLIENT","clientename")
# ELASTIC_ENV =  os.environ.get("ENVIRONMENT", "dev")
#PUBLISH_TO_ELASTIC = os.environ.get("PUBLISH_TO_ELASTIC",True)
# PUBLISH_TO_ELASTIC = True

TIMEZONE = os.environ.get("TIMEZONE","America/Sao_Paulo")
# ELASTIC_HOST =  os.environ.get("ELASTICSEARCH_HOST", None)
# ELASTIC_USER =  os.environ.get("ELASTIC_USER", None)
# ELASTIC_PWD =  os.environ.get("ELASTIC_PWD", None)
OUTPUT_LOG = "Output/Logs"

output_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"

class Logger():
    
    def __init__(self) -> None:
        pass
    
    def __add_kwargs_in_log(self, kwargs, args = "") -> str:
        count = 0
        for key, value in kwargs.items():
            count += 1
            if len(kwargs.items()) > 1:
                if count < len(kwargs.items()):
                    args += f"{key}={value} | "
                else:
                    args += f"{key}={value}"
            else:
                args += f"{key}={value}"
        return args
        
    def _message(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = message
        if traceId:
            msg = f"ID: {traceId} | {message}"
        
        args = self.__add_kwargs_in_log(kwargs)
        if args == "":
            msg = args if message == '' else f'{msg}'
        else:
            msg = args if message == '' else f'{msg} | {args}'
        return msg

    def _create_file_log(self, datetime_now, log_per_day: bool = False) -> str:
        if log_per_day:
            # cria um arquivo de log por dia
            return f"{OUTPUT_LOG}/{datetime_now.strftime('%Y-%m-%d')}.log"
        else:
            # cria um arquivo de log por mensagem de log
            return f"{OUTPUT_LOG}/{datetime_now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.log"
        
    def __verify_file_extension(self, filename: str) -> bool:
        if '.txt' in filename[-4:]:
            return f"{OUTPUT_LOG}/{filename}"                
        if '.log' in filename[-4:]:
            return f"{OUTPUT_LOG}/{filename}"
        if not '.log' in filename[-4:] or not '.txt' in filename[-4:]:
            return f"{OUTPUT_LOG}/{filename}.log"
        else:
            return f"{OUTPUT_LOG}/{filename}.txt"
           
    def _filename(self, filename: str = None, log_per_day: bool = True) -> str:
        if filename == None:
            return self._create_file_log(datetime.now(), log_per_day)
        else:
            return self.__verify_file_extension(filename)
    
    def __log(self, 
              level, 
              message: str = '', 
              traceId: Optional[str] = None, 
              log_format: str = output_log_format,
              log_per_day: bool = True,  
              **kwargs: Any) -> None:
        logging.basicConfig(filename=self._filename(log_per_day=log_per_day), level=level, format=f"{log_format}")
        msg = self._message(message, traceId=traceId, **kwargs)
        return msg
    
    def log_debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.debug(self.__log(level=logging.DEBUG, message=message, traceId=traceId, **kwargs))
        
    def log_info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.info(self.__log(level=logging.INFO, message=message, traceId=traceId, **kwargs))
        
    def log_warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.warning(self.__log(level=logging.WARNING, message=message, traceId=traceId, **kwargs))
        
    def log_error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.error(self.__log(level=logging.ERROR, message=message, traceId=traceId, **kwargs))
        
    def log_critical(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        logging.critical(self.__log(level=logging.CRITICAL, message=message, traceId=traceId, **kwargs))
            
            
class __OLD_Logger:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self) -> None:
        # self.ROBOT_LIBRARY_LISTENER = self
        self.PUBLISH_TO_ELASTIC = True
        self.CLIENT = CLIENT
        self.ROBOT_NAME = ROBOT_NAME

        #if self.PUBLISH_TO_ELASTIC:
        # self.el = Elastic(client=self.CLIENT, robot_name=self.ROBOT_NAME)

    def start_suite(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            totaltasks=attributes['totaltests'],
            tasks=str(attributes['tests']),
            doc=attributes['doc'],
            starttime=attributes['starttime'],
            trigger_type='start_suite'
        )
        self.log_info(**info)


    def start_test(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            doc=attributes['doc'],
            starttime=attributes['starttime'],
            trigger_type='start_task'
        )
        self.log_info(**info)

    def start_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            doc=attributes['doc'],
            args=str(attributes['args']),
            starttime=attributes['starttime'],
            trigger_type='start_keyword'
        )
        self.log_info(**info)


    def log_message(self, message: dict):
        """Listener Function"""
        message['trigger_type']='log_message'
        self.log_info(**message)


    def end_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            trigger_type='end_keyword'
        )
        self.log_info(**info)


    def end_test(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            sys_message=attributes['message'],
            trigger_type='end_task'
        )
        self.log_info(**info)


    def end_suite(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            statistics=attributes['statistics'],
            sys_message=attributes['message'],
            trigger_type='end_suite'
        )
        self.log_info(**info)


class __Elastic:
    tz = pytz.timezone(TIMEZONE)

    def __init__(self, client: str, robot_name: str) -> None:
        self.CLIENT = client
        self.ROBOT_NAME = robot_name

        self.ENV = ELASTIC_ENV
        self.HOST = ELASTIC_HOST
        self.USER = ELASTIC_USER
        self.PWD = ELASTIC_PWD

        self.es = Elasticsearch(
            hosts=self.HOST,
            http_auth=(self.USER, self.PWD)
        )
        self.index = datetime.today().strftime(
            "robot-logs-{}-{}-{}-%Y.%m"
            .format(
                self.ENV,
                self.CLIENT,
                self.ROBOT_NAME
            )
        )


    def publish(self, message: str, **fields: Any) -> None:
        if not PUBLISH_TO_ELASTIC:
            return

        timestamp = datetime.now(self.tz)

        protected_keys = ['pwd','psw','password','senha','secret']
        for key in protected_keys:
            if key in fields:
                del fields[key]

        fields['robot_name'] = self.ROBOT_NAME

        doc = {
            "message": message,
            "timestamp": timestamp
        }
        try:
            for key, value in fields.items():
                if key == 'timestamp':
                    value = datetime.strptime(value, '%Y%m%d %H:%M:%S.%f')
                doc.update({key: value})
            resultado = self.es.index(
                index=self.index, body=doc)
            #logger.error(f'Resultado: ${resultado}')
            return resultado
        except Exception as e:
            logger.error(
                f"Erro ao tentar logar no ElasticSearch. Detalhes: {e}",
                html=True
            )