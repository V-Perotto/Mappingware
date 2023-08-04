from time import sleep
from os import getcwd, startfile, path
from json import load
from win32com.client import Dispatch

from Monitor.MicrosoftTeams import MicrosoftTeams
from Monitor.Message import Message
from Monitor.Services import Services
from Monitor.Machine import Machine
from Monitor.Connectivity import Connectivity
from Monitor.Telegram import Telegram

class Checker():
    
    def check_machine(self):
        """
            Função que faz a verificação dos recursos da máquina.
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
            self.run_disk_cleaner_script()
            resources.update({'ram':ram})
                
        if resources:
            m = Message(servidor=servidor, resources=resources).mensagem_recurso()
            Telegram(bot_id=bot_id, chat_id=chat_id, message=m).send_telegram_message()
            MicrosoftTeams().sendMessage(m)
            print(f'Machine {servidor} with high usage of resources!!!')
            print(resources)
            print('')

    def check_service(self, name, host=None, port=None):
        """
            Função que checa se um serviço (seja um serviço do Windows ou uma aplicação tcp/ip) está ativo ou em estado de listening.

            :param name: nome da aplicacao
            :type name: string
            :param host: nome ou endereço IP, defaults to None
            :type host: string, optional
            :param port: porta, defaults to None
            :type port: string, optional
        """
        service = Services(name)
        if name == 'GoogleDrive':
            is_drive_running = self.check_google_drive()
            if not is_drive_running:
                m = Message(servico=name,servidor=servidor).mensagem_indisponibilidade()
                Telegram(bot_id=bot_id, chat_id=chat_id, message=m).send_telegram_message()
                MicrosoftTeams().sendMessage(m)
                print(f'Service \'{name}\' unavailable!!!')
                print("Iniciando serviço")
                startfile('"C:\Program Files\Google\Drive File Stream\launch.bat"')
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

    def _check_existence_by_path_language(self):
        """
            Checar a existencia do caminho da linguagem em especifico

            Returns:
                bool: True/False
        """
        try:
            english_path_exists = path.exists(r"G:\My Drive")
            portuguese_path_exists = path.exists(r"G:\Meu Drive")
            if not portuguese_path_exists and not english_path_exists:
                return False
            if not portuguese_path_exists or not english_path_exists:
                return True
        except Exception as e:
            print(f'Erro ao carregar um dos possíveis diretórios do Google Drive! {e}')
            return False

    def check_google_drive(self):
        """
            Checar o Google Drive

            Returns:
                bool: True/False
        """
        try:
            google_path_exists = self._check_existence_by_path_language()
            if not google_path_exists:
                print("Google Drive não está ativo!")
            if google_path_exists:
                print("Google Drive está ativo.")
            return google_path_exists
        except Exception as e:
            print(f'Erro ao carregar o diretório do Google Drive! {e}')
            return False
        
    def load_config(self):
        """
            Função que carrega o arquivo de configurações utilizado na parametrização do monitoramento.

            :return: retorna True se o carregamento (leitura do arquivo) teve êxito ou False caso contrário.
            :rtype: bool
        """
        home = getcwd()
        try: 
            print('Carregando o arquivo de configuração!')
            global ms_teams_webhook, bot_id, chat_id, cpu_percent_threshold, ram_percent_threshold, disk_percent_threshold
            with open(rf"{home}/config.json") as json_file:
                data = load(json_file)
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

    def check(self):
        """
            Função que chama os métodos responsáveis por realizar o monitoramento.
        """
        print('Iniciando monitoramento...')
        while 1:
            print('Coletando dados')
            self.check_machine()
            self.check_service('GoogleDrive')
            self.check_service('MongoDB','127.0.0.1','27017')
            self.check_service('Vault','127.0.0.1','8200')
            self.check_service('ElasticSearch','127.0.0.1','9200')
            self.check_service('Kibana','127.0.0.1','5601')
            sleep(30)
            print('')

    def run_disk_cleaner_script(self):
        """
            Função que dispara o log rotate para fazer a limpeza dos arquivos em disco.
        """
        try:
            print("executando limpeza no disco")
            task_name = 'log-rotate'
            scheduler = Dispatch('Schedule.Service')
            scheduler.Connect()
            rootFolder = scheduler.GetFolder('\\RPA_TOOLS')
            task = rootFolder.GetTask(task_name)
            task.Enabled = True
            runningTask = task.Run("")
        except:
            print(f"Não foi possível executar o script {task_name}")
        
    def main(self):
        config = self.load_config()
        if config:
            self.check()

if __name__ == "__main__":
    Checker().main()