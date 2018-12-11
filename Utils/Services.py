import time
import datetime
from auth.auth_request import AuthRequest
class Services(object):
    url = None
    user = None
    password = None
    token = None
    expiration_date = 0

    def __init__(self, url, token = None, user = None, password = None):
        if url:
            self.url = url
        else:
            print("Se debe definir URL")
        if user and password:
            self.user = user
            self.password = password
        else:
            if token:
                self.token = token
                self.expiration_date = 9999999999
            else:
                print("Se debe definir user y password o token")

    def get_token(self):
        if not self.token or datetime.datetime.now().timestamp() > self.expiration_date:
            auth_obj = AuthRequest.authenticate(self.url, self.user, self.password)
            self.token = auth_obj.get_token()
            self.expiration_date = int(auth_obj.get_time_expire())
        return self.token
    @staticmethod
    def get_url(self):
        return self.url
    @staticmethod
    def get_user(self):
        return self.user
    @staticmethod
    def get_password(self):
        return self.password
