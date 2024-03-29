from Auth.AuthRequest import AuthRequest
from Utils.Services import Services

class Auth(Services):
    def __init__(self, url, token, user, password):
        super(Auth, self).__init__(url, None, user, password)
    
    def authentication(self):
        return AuthRequest.authenticate(self.get_url(), self.get_user(), self.get_password())
