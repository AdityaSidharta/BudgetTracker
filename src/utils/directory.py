import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(PROJECT_PATH, "data")
ENV_PATH = os.path.join(PROJECT_PATH, "env")

CREDENTIALS_PATH = os.path.join(ENV_PATH, "gcloud.json")
SECRETENV_PATH = os.path.join(ENV_PATH, "secret.env")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH