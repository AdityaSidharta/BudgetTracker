import os

from dotenv import load_dotenv

from src.utils.directory import SECRETENV_PATH


class Config:
    def __init__(self):
        load_dotenv(dotenv_path=SECRETENV_PATH, verbose=True)
        self.BUCKET_NAME = os.getenv("BUCKET_NAME")
        self.APP_ID = os.getenv('APP_ID')
        self.SECRET = os.getenv('SECRET')
        self.CUSTOMER_ID = '1'

config = Config()
