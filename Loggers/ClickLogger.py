import time

class ClickLogger:
    
    def __init__(self) -> None:
        self.clicks = []
        
    def log_click(self, button_name) -> None:
        timestamp = time.time()
        self.clicks.append((timestamp, button_name))
        
    def get_clicks(self) -> list:
        return self.clicks