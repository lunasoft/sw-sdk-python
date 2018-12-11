from auth.auth_request import AuthRequest 
from utils.services import Services

class Auth(Services):
    def __init__(self, url, token, user, password):
        super(Auth, self).__init__(url, None, user, password)
    
    def authentication(self):
        return AuthRequest.authenticate(self.url, self.user, self.password)
