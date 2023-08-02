from datetime import datetime
from jinja2 import Template

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