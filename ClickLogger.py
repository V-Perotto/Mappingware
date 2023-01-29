import time

class ClickLogger:
    def __init__(self):
        self.clicks = []
        
    def log_click(self, button_name):
        timestamp = time.time()
        self.clicks.append((timestamp, button_name))
        
    def get_clicks(self):
        return self.clicks