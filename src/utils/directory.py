import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
ENV_PATH = os.path.join(PROJECT_PATH, "env")
CONFIG_PATH = os.path.join(PROJECT_PATH, "config")

RAW_PATH = os.path.join(DATA_PATH, "raw")
FINAL_PATH = os.path.join(DATA_PATH, "final")

CONFIG_YAML_PATH = os.path.join(CONFIG_PATH, "config.yaml")
EXPENSE_YAML_PATH = os.path.join(CONFIG_PATH, "expense.yaml")
INCOME_YAML_PATH = os.path.join(CONFIG_PATH, "income.yaml")