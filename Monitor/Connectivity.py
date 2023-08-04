from os import system
from socket import socket, AF_INET, SOCK_STREAM

class Connectivity():
    """
        Classe de conectividade. Contem os métodos relativos a conectividade, como checar se porta está aberta
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
            a_socket = socket(AF_INET, SOCK_STREAM)
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
        response = system("ping -n 1 " + self.host + " -w 500")
        if response == 0:
            return True
        else:
            return False