from Auth.AuthRequest import AuthRequest 
from Utils.Services import Services#Package.File import class

class Auth(Services):
    def __init__(self, url, token, user, password):
        super(Auth,self).__init__(url, None, user, password)
    
    def Authentication(self):
        return AuthRequest.authenticate(self.url, self.user, self.password)
