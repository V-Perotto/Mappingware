import os
from pathlib import Path

ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)
OUTPUT_LOG = os.path.join(ROOT, "Output/Logs")