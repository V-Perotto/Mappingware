from os import path
from pathlib import Path

ROOT = str(Path(path.dirname(path.abspath(__file__))).parent)
OUTPUT_LOG = path.join(ROOT, "Output/Logs")
OUTPUT_JSON = path.join(OUTPUT_LOG, "Json") 
keyboard_mouse = "Keyboard_Mouse"
