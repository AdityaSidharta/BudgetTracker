import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
ENV_PATH = os.path.join(PROJECT_PATH, "env")

RAW_PATH = os.path.join(DATA_PATH, "raw")
FINAL_PATH = os.path.join(DATA_PATH, "final")
