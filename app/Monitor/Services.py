import os
import psutil
import json
import win32com.client
import win32serviceutil

class Services():
    """
        Classe de serviços. Contem os métodos que interagem com os serviços do Windows.
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