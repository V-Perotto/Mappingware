from pymsteams import connectorcard    # pip install pymsteams

class MicrosoftTeams():
    
    def __init__(self):
        self.connector = connectorcard("link_do_teams_webhook")
        
    def sendMessage(self, message):
        self.connector.text(message.replace('</b>','').replace('<b>',''))
        self.connector.send()