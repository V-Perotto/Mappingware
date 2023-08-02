import requests as request

class Telegram():
    """
        Classe que contem os métodos utilizados pela mensageria do Telegram.
    """
    def __init__(self, **kwargs):
        self.endpoint = "https://api.telegram.org/"
        for key, value in kwargs.items():
            setattr(self, key, value)

    def send_telegram_message(self):
        """
            Efetua o envio de uma mensagem pelo Telegram.

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