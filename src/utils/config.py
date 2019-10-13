import os

from dotenv import load_dotenv
from src.utils.directory import ENV_PATH


class Config:
    def __init__(self):
        self.CREDENTIALS_PATH = os.path.join(ENV_PATH, "gcloud.json")
        self.SECRETENV_PATH = os.path.join(ENV_PATH, "saltedge.env")

        if os.path.isfile(self.CREDENTIALS_PATH):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.CREDENTIALS_PATH
            self.BUCKET_NAME = 'saltedgepython'
            self.gcs_backup = True
        else:
            self.gcs_backup = False

        if os.path.isfile(self.SECRETENV_PATH):
            load_dotenv(self.SECRETENV_PATH)
            self.APP_ID = os.getenv('APP_ID')
            self.SECRET = os.getenv('SECRET')
            self.CUSTOMER_NAME = 'saltedgepython'
        else:
            raise ValueError('saltedge.env must be created. please follow README for the instructions.')

        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'App-id': self.APP_ID,
            'Secret': self.SECRET
        }


config = Config()
