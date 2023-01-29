from pynput import keyboard

class KeyLogger:

    def on_press(key) -> str:
        return f"{key} pressed"

    def on_release(key) -> str:
        return f"{key} released"
        
    def keyboard_listener(on_press, on_release) -> None:    
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()