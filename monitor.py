import requests as request
import psutil
import socket
import os
import time
import json
from datetime import datetime
from jinja2 import Template
import pymsteams
import win32com.client
import json
import win32serviceutil
import os

class Services():
    """Classe de serviços. Contem os métodos que interagem com os serviços do Windows.
    """
    def __init__(self, name):
        self.name = name
        self.home_path = os.getcwd()
        self.path_config = rf"{self.home_path}\config.json"

    def find_win_service(self):
        """Efetua a busca de um serviço

        :return: retorna True se o serviço foi encontrado ou False caso contrário.
        :rtype: bool
        """
        try:
            return psutil.win_service_get(self.name)
        except psutil.NoSuchProcess as e:
            print(f"Service {self.name} not found!")
            return False

    def running_state(self):
        """Checa se o serviço está rodando.

        :return: retorna True se o serviço está em execução (running) ou False caso contrário.
        :rtype: bool
        """
        try:
            status = self.find_win_service().status()
            if status == "running":
                return True
            else:
                return False
        except AttributeError as e:
            print(f"Service {self.name} not found!")
            return False

    def init_service(self,name):
        """
        Função que dispara a task do serviço que não está ativo
        """
        print("carregando configurações")
        self.config_init_services = json.loads(open(self.path_config,"r").read())["init_service_config"]
        if name not in self.config_init_services.keys():
            print("Serviço Externo ou não configurado em -> config.json")
            return False
        
        config = self.config_init_services[name]
        
        if config["type_init"] == "windows_task_scheduler":
            try:
                print(f"Iniciando {name}")
                scheduler = win32com.client.Dispatch('Schedule.Service')
                scheduler.Connect()
                rootFolder = scheduler.GetFolder(config["folder"])
                task = rootFolder.GetTask(config["name_task"])
            except:
                print("task não existe")
                return False

            # task.Enabled = True
            runningTask = task.Run("")
            print(f"task executada com sucesso {runningTask}")
        
        if config["type_init"] == "windows_services":
            print("iniciando serviço")
            name_service = config["name_service"]
            try: 
                win32serviceutil.StartService(name_service)
            except Exception as e:
                print(f"Erro ao tentar iniciar o serviço do {name}")
                print(e)
                return False

            print(f"O serviço do {name} foi iniciado com sucesso")

class Connectivity():
    """Classe de conectividade. Contem os métodos relativos a conectividade, como checar se porta está aberta
    ou se o destino responde ICMP (check_ping).
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    def check_connectivity(self):
        """Checa se uma determinada porta de um host está comunicável (listening port).

        :return: retorna True se a porta está comunicável ou False caso contrário.
        :rtype: bool
        """
        try:
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            location = (self.host, int(self.port))
            result_of_check = a_socket.connect_ex(location)
            if result_of_check == 0:
               return True
            else:
               return False
            a_socket.close()
        except:
            return False

    def check_ping(self):
        """Checa se um determinado host (nome ou endereço IP), responde a requisições ICMP (ping)

        :return: retorna True se o host está respondendo aos pings (echo reply) ou False caso contrário.
        :rtype: bool
        """
        response = os.system("ping -n 1 " + self.host + " -w 500")
        if response == 0:
            return True
        else:
            return False

class Machine():
    """Classe que contem os métodos relacionados aos recursos da máquina.
    """
    def __init__(self):
        self.raw_cpu_usage = psutil.cpu_times_percent(interval=0.4, percpu=False)
        self.raw_memory = psutil.virtual_memory()
        self.raw_disk_usage = psutil.disk_usage(".")
        self.user_unlock()

    def return_hostname(self):
        """Retorna o hostname da máquina

        :return: retorna o nome da máquina
        :rtype: string
        """
        return os.environ['COMPUTERNAME']

    def return_cpu_usage(self):
        """Retorna o uso atual de CPU.

        :return: retorna o uso de cpu (porcentagem) como string
        :rtype: float
        """
        return self.raw_cpu_usage.interrupt + self.raw_cpu_usage.system

    def return_ram_usage_percent(self):
        """Retorna o uso atual de Memória RAM.

        :return: retorna o uso de RAM (porcentagem) como string
        :rtype: float
        """
        return self.raw_memory.percent

    def return_ram_usage_in_GB(self):
        """Retorna o uso atual de Memória RAM em Gigabytes.

        :return: retorna o uso de RAM em GB.
        :rtype: float
        """
        return self.raw_memory.used / 1024 / 1024 / 1024

    def return_disk_free_in_GB(self):
        """Retorna a quantidade de espaço livre do disco em Gigabytes.

        :return: retorna a quantidade livre em GB.
        :rtype: float
        """
        return self.raw_disk_usage.free / 1024 / 1024 / 1024

    def return_disk_usage_percent(self):
        """Retorna a porcentagem de uso de disco (espaço armazenado x espaço total).

        :return: retorna em porcentagem o uso de disco em GB.
        :rtype: float
        """
        return self.raw_disk_usage.percent

    def user_unlock (self):
        """
            Funçao para desbloquear usuario de dev no servidor
        """
        try:        
            stream = os.popen('Net user usr_dev /ACTIVE:YES')
            stream.read()
        except Exception as e:
            print(f"Erro ao desbloquear usuario: {e}")
class Telegram():
    """Classe que contem os métodos utilizados pela mensageria do Telegram.
    """
    def __init__(self, **kwargs):
        self.endpoint = "https://api.telegram.org/"
        for key, value in kwargs.items():
            setattr(self, key, value)

    def send_telegram_message(self):
        """Efetua o envio de uma mensagem pelo Telegram.

        :return: retorna True se teve êxito ou False caso contrário.
        :rtype: bool
        """
        method = "sendMessage"
        try:
            url_request = self.endpoint + self.bot_id+'/'+ method + \
            '?chat_id=' + self.chat_id + '&text=' + self.message + '&parse_mode=HTML'
            response = request.get(url_request)
            return True, response
        except:
            return False

class Message():
    """Classe que contem os métodos de formatação e criação das mensagens de notificação.
    """
    def __init__(self, **kwargs):
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def mensagem_indisponibilidade(self):
        """Efetua a criação e formatação da mensagem de indisponibilidade de um serviço.

        :return: retorna string contendo a mensagem formatada
        :rtype: string
        """
        mensagem_indisponibilidade = f"""
        <b>Alerta de indisponibilidade!</b>
        <b>Serviço: </b> {self.servico}
        <b>Data: </b> {self.data}
        <b>Servidor: </b>{self.servidor}
        """
        return mensagem_indisponibilidade

    def mensagem_recurso(self):
        """Efetua a criação e formatação da mensagem de utilização de recursos.

        :return: retorna string contendo a mensagem formatada
        :rtype: string
        """
        base_mensagem_recurso = """
        <b>Alerta de recursos!</b>
        {% for key, value in recursos.items() %}
            <b>{{key}}: </b> {{value}}%
        {% endfor %}
        <b>Data: </b> {{data}}
        <b>Servidor: </b>{{servidor}}
        """
        template=Template(base_mensagem_recurso)
        mensagem_recurso=template.render(recursos=self.resources,data=self.data,servidor=self.servidor)
        return mensagem_recurso

class MicrosoftTeams():
    def __init__(self):
        self.connector = pymsteams.connectorcard("link_do_teams_webhook")
        
    def sendMessage(self, message):
        self.connector.text(message.replace('</b>','').replace('<b>',''))
        self.connector.send()
  
def check_machine():
    """Função que faz a verificação dos recursos da máquina.
    """
    maquina = Machine()
    global servidor
    servidor = maquina.return_hostname()
    resources = {}
    cpu = maquina.return_cpu_usage()
    ram = maquina.return_ram_usage_percent()
    disk = maquina.return_disk_usage_percent()
    
    print(disk)

    if cpu > cpu_percent_threshold:
        resources.update({'cpu':cpu})

    if ram > ram_percent_threshold:
        resources.update({'ram':ram})

    if disk > disk_percent_threshold:
        run_disk_cleaner_script()
        resources.update({'ram':ram})
            
    if resources:
        m = Message(servidor=servidor, resources=resources).mensagem_recurso()
        Telegram(bot_id=bot_id, chat_id=chat_id, message=m).send_telegram_message()
        MicrosoftTeams().sendMessage(m)
        print(f'Machine {servidor} with high usage of resources!!!')
        print(resources)
        print('')

def check_service(name, host=None, port=None):
    """Função que checa se um serviço (seja um serviço do Windows ou uma aplicação tcp/ip) está ativo ou em estado de listening.

    :param name: nome da aplicacao
    :type name: string
    :param host: nome ou endereço IP, defaults to None
    :type host: string, optional
    :param port: porta, defaults to None
    :type port: string, optional
    """
    service = Services(name)
    if name == 'GoogleDrive':
        is_drive_running = check_google_drive()
        if not is_drive_running:
            m = Message(servico=name,servidor=servidor).mensagem_indisponibilidade()
            Telegram(bot_id=bot_id, chat_id=chat_id, message=m).send_telegram_message()
            MicrosoftTeams().sendMessage(m)
            print(f'Service \'{name}\' unavailable!!!')
            print("Iniciando serviço")
            os.startfile('"C:\Program Files\Google\Drive File Stream\launch.bat"')
            return m
    else:
        is_listening = is_running = True
        if ((host and port) is not None):
            is_listening = Connectivity(host=host,port=port).check_connectivity()
        else:
            is_running = service.running_state()
        if not is_running or not is_listening:
            m = Message(servico=name,servidor=servidor).mensagem_indisponibilidade()
            Telegram(bot_id=bot_id, chat_id=chat_id, message=m).send_telegram_message()
            MicrosoftTeams().sendMessage(m)
            print(f'Service \'{name}\' unavailable!!!')
            print("Iniciando serviço")
            service.init_service(name)            
            return m
        else:
            print(f'Service \'{name}\' is running!')
        print('')

def _check_existence_by_path_language():
    try:
        english_path_exists = os.path.exists(r"G:\My Drive")
        portuguese_path_exists = os.path.exists(r"G:\Meu Drive")
        if not portuguese_path_exists and not english_path_exists:
            return False
        if not portuguese_path_exists or not english_path_exists:
            return True
    except Exception as e:
        print(f'Erro ao carregar um dos possíveis diretórios do Google Drive! {e}')
        return False

def check_google_drive():
    try:
        google_path_exists = _check_existence_by_path_language()
        if not google_path_exists:
            print("Google Drive não está ativo!")
        if google_path_exists:
            print("Google Drive está ativo.")
        return google_path_exists
    except Exception as e:
        print(f'Erro ao carregar o diretório do Google Drive! {e}')
        return False
    
def load_config():
    """Função que carrega o arquivo de configurações utilizado na parametrização do monitoramento.

    :return: retorna True se o carregamento (leitura do arquivo) teve êxito ou False caso contrário.
    :rtype: bool
    """
    home = os.getcwd()
    try: 
        print('Carregando o arquivo de configuração!')
        global ms_teams_webhook, bot_id, chat_id, cpu_percent_threshold, ram_percent_threshold, disk_percent_threshold
        with open(rf"{home}/config.json") as json_file:
            data = json.load(json_file)
            for config in data['config']:
                ms_teams_webhook = config['ms_teams_webhook']
                bot_id = config['bot_id']
                chat_id = config['chat_id']
                cpu_percent_threshold = config['cpu_percent_threshold']
                ram_percent_threshold = config['ram_percent_threshold']
                disk_percent_threshold = config['disk_percent_threshold']
        return True
    except Exception as e:
        print(f'Erro ao carregar o arquivo de configuração! {e}')
        return False


def check():
    """Função que chama os métodos responsáveis por realizar o monitoramento.
    """
    print('Iniciando monitoramento...')
    while 1:
        print('Coletando dados')
        check_machine()
        check_service('GoogleDrive')
        check_service('MongoDB','127.0.0.1','27017')
        check_service('Vault','127.0.0.1','8200')
        check_service('ElasticSearch','127.0.0.1','9200')
        check_service('Kibana','127.0.0.1','5601')
        time.sleep(30)
        print('')

def run_disk_cleaner_script():
    """
     Função que dispara o log rotate para fazer a limpeza dos arquivos em disco.
    """
    try:
        print("executando limpeza no disco")
        task_name = 'log-rotate'
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        rootFolder = scheduler.GetFolder('\\RPA_TOOLS')
        task = rootFolder.GetTask(task_name)
        task.Enabled = True
        runningTask = task.Run("")
    except:
        print(f"Não foi possível executar o script {task_name}")
    
def main():
    config = load_config()
    if config:
        check()

if __name__ == "__main__":
    main()