from pendings.pendings_request import PendingsRequest
from utils.services import Services

class Pendings(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Pendings, self).__init__(url, token, user, password)
    
    def pendings(self, rfc):
        return PendingsRequest.pendings_rfc(self.url, self.token, rfc)