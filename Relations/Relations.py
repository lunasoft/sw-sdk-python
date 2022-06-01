from Relations.RelationsRequest import RelationsRequest
from Utils.Services import Services

class Relations(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Relations, self).__init__(url, token, user, password)

    def relations_csd(self, rfc, uuid, b64_cert, b64_key, password):
        return RelationsRequest.relations_csd(self.get_url(), self.get_token(), rfc, uuid, b64_cert, b64_key, password)
    
    def relations_pfx(self, rfc, uuid, b64_pfx, password):
        return RelationsRequest.relations_pfx(self.get_url(), self.get_token(), rfc, uuid, b64_pfx, password)

    def relations_uuid(self, rfc, uuid):
        return RelationsRequest.relations_uuid(self.get_url(), self.get_token(), rfc, uuid)
