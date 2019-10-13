import os

from dotenv import load_dotenv

from src.utils.directory import SECRETENV_PATH


class Config:
    def __init__(self):
        self.CREDENTIALS_PATH = os.path.join(ENV_PATH, "gcloud.json")
        self.SECRETENV_PATH = os.path.join(ENV_PATH, "saltedge.env")

        if os.path.isfile(self.CREDENTIALS_PATH):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.CREDENTIALS_PATH
            self.BUCKET_NAME = 'saltedge-python'
            self.gcs_backup = True
        else:
            self.gcs_backup = False

        if os.path.isfile(self.CREDENTIALS_PATH):
            load_dotenv(self.SECRETENV_PATH)
            self.APP_ID = os.getenv('APP_ID')
            self.SECRET = os.getenv('SECRET')
            self.CUSTOMER_ID = '1'
        else:
            raise ValueError('saltedge.env must be created. please follow README for the instructions.')

        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'App-id': config.APP_ID,
            'Secret': config.SECRET
        }


config = Config()
