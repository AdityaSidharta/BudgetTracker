import os

import joblib
from google.cloud import storage
from loguru import logger

from src.utils.directory import CREDENTIALS_PATH, DATA_PATH
from src.utils.config import config


class Storage:
    def __init__(self):

        self.storage_client = storage.Client()
        self.bucket_name = config.BUCKET_NAME
        self.bucket = self.storage_client.get_bucket(self.bucket_name)
        self.logger = logger

    def list(self):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        return [blob.name for blob in blobs]

    def upload(self, path):
        remote_path = path
        local_path = os.path.join(DATA_PATH, path)
        if self.exist(path):
            self.logger.warning("Overwriting the remote file {}/{}".format(local_path, self.bucket_name, path))
        blob = self.bucket.blob(remote_path)
        blob.upload_from_filename(local_path)
        self.logger.info("Uploading from local:{} to remote:{}/{}".format(local_path, self.bucket_name, path))

    def download(self, path):
        if self.exist(path):
            remote_path = path
            local_path = os.path.join(DATA_PATH, path)
            if not os.path.exists(os.path.dirname(local_path)):
                os.makedirs(os.path.dirname(local_path))
            blob = self.bucket.blob(remote_path)
            blob.download_to_filename(local_path)
            self.logger.info("Downloading from remote:{}/{} to {}".format(self.bucket_name, path, local_path))
            success = True
        else:
            success = False
        return success

    def exist(self, path):
        blobs = self.list()
        return path in blobs

    def read(self, path, keep=True):
        success = self.download(path)
        if success:
            local_path = os.path.join(DATA_PATH, path)
            blob = joblib.load(local_path)
            if not keep:
                os.remove(local_path)
            return blob
        else:
            raise ValueError("File Does not Exist")

    def write(self, blob, path, keep=True):
        local_path = os.path.join(DATA_PATH, path)
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        joblib.dump(blob, local_path)
        self.upload(path)
        if not keep:
            os.remove(local_path)
