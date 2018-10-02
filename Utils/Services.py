import time
import datetime
from Auth.AuthRequest import AuthRequest
class Services(object):
    url = None
    user = None
    password = None
    token = None
    expirationDate = int("9999999999")

    def __init__(self, url, token=None, user=None, password=None):
        if url:
            self.url = url
        else:
            print("Se debe definir URL")
        if user and password:
            self.user = user
            self.password = password
            authobj = AuthRequest.authenticate(self.url, self.user, self.password)
            self.token = authobj.getToken()
            self.expirationDate = int(authobj.getTimeExpire())
        else:
            if token:
                self.token = token
            else:
                print("Se debe definir user y password o token")

    def getToken(self):
        if not self.token or datetime.datetime.now().timestamp() > self.expirationDate:
            authobj = AuthRequest.authenticate(self.url, self.user, self.password)
            self.token = authobj.getToken()
        return self.token
    @staticmethod
    def getUrl(self):
        return self.url
    @staticmethod
    def getUser(self):
        return self.user
    @staticmethod
    def getPassword(self):
        return self.password
