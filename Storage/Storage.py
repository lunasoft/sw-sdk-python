from Storage.StorageRequest import StorageRequest
from Utils.Services import Services

class Storage(Services):
    url_api = None
    def __init__(self, url, url_api, token = None, user = None, password = None):
        super(Storage, self).__init__(url, token, user, password)
        if not url_api:
            raise ValueError("Debe especificar la url_api")
        self.url_api = url_api

    def get_by_uuid(self, uuid):
        return StorageRequest.get_by_uuid(self.url_api, self.get_token(), uuid)
