import os
from typing import Any, Optional
from datetime import datetime
import pytz
from robot.api import logger
from elasticsearch import Elasticsearch

ROBOT_NAME = os.environ.get("ROBOT_NAME","roboname")
CLIENT = os.environ.get("CLIENT","clientename")
ELASTIC_ENV =  os.environ.get("ENVIRONMENT", "dev")
#PUBLISH_TO_ELASTIC = os.environ.get("PUBLISH_TO_ELASTIC",True)
PUBLISH_TO_ELASTIC = True

TIMEZONE = os.environ.get("TIMEZONE","America/Sao_Paulo")
ELASTIC_HOST =  os.environ.get("ELASTICSEARCH_HOST", None)
ELASTIC_USER =  os.environ.get("ELASTIC_USER", None)
ELASTIC_PWD =  os.environ.get("ELASTIC_PWD", None)

class Logger:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self) -> None:
        # self.ROBOT_LIBRARY_LISTENER = self
        self.PUBLISH_TO_ELASTIC = True
        self.CLIENT = CLIENT
        self.ROBOT_NAME = ROBOT_NAME

        #if self.PUBLISH_TO_ELASTIC:
        self.el = Elastic(client=self.CLIENT, robot_name=self.ROBOT_NAME)

    def log_info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        also_console = True
        if 'console' in kwargs:
            also_console = kwargs['console']
        logger.info(msg, html=True, also_console=also_console)
        if 'level' not in kwargs:
            kwargs['level'] = 'INFO'
        self.el.publish(msg, traceId=traceId, **kwargs)

    def log_warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.warn(msg, html=True)
        self.el.publish(msg, traceId=traceId, level="WARN", **kwargs)

    def log_debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.debug(msg, html=True)
        self.el.publish(msg, traceId=traceId, level="DEBUG", **kwargs)

    def log_error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.error(msg, html=True)
        self.el.publish(msg, traceId=traceId, level="ERROR", **kwargs)

    def _message(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        msg = message
        args = ""
        if traceId:
            msg = f"ID: {traceId} | {message}"
        for key, value in kwargs.items():
            args += f" {key}={value}"
        # TODO achar de onde ta vindo o dicinário na 'message'
        #try:
        #    msg = args if message.strip() == '' else f'{msg} | {args}'
        #except:
        #    msg = args if message == '' else f'{msg} | {args}'
        msg = args if message == '' else f'{msg} | {args}'
        return msg

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


class Elastic:
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