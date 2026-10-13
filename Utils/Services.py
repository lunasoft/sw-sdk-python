import time
import datetime
from Auth.AuthRequest import AuthRequest
class Services(object):
    url = None
    user = None
    password = None
    token = None
    expiration_date = 0

    def __init__(self, url, token = None, user = None, password = None):
        if not url:
            raise ValueError("Se debe definir URL")
        self.url = url
        if user and password:
            self.user = user
            self.password = password
        elif token:
            self.token = token
            self.expiration_date = 9999999999
        else:
            raise ValueError("Se debe definir user y password o token")

    def get_token(self):
        if not self.token or datetime.datetime.now().timestamp() > self.expiration_date:
            auth_obj = AuthRequest.authenticate(self.url, self.user, self.password)
            if auth_obj.get_status() == "success":
                self.token = auth_obj.get_token()
                self.expiration_date = int(auth_obj.get_time_expire())
            else:
                raise ValueError(f"Error de autentificación: {auth_obj.get_message()}")
        return self.token

    def get_url(self):
        return self.url

    def get_user(self):
        return self.user
        
    def get_password(self):
        return self.password
    