from Storage.StorageRequest import StorageRequest
from Utils.Services import Services

class Storage(Services):
    urlApi = None
    def __init__(self, url, urlApi, token = None, user = None, password = None):
        super(Storage, self).__init__(url, token, user, password)
        if urlApi:
            self.urlApi = urlApi
        else:
            print("Debe especificar la urlApi")

    def get_by_uuid(self, uuid):
        return StorageRequest.get_by_uuid(self.urlApi, self.get_token(), uuid)
