from Relations.RelationsRequest import RelationsRequest
from Utils.Services import Services

class Relations(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Relations,self).__init__(url, token, user, password)
    
    def RelationsXml(self, xmlCancel):
        return RelationsRequest.relations_by_xml(self.url, self.token, xmlCancel)

    def RelationsCsd(self, rfc, uuid, b64cert, b64key, cPassword):
        return RelationsRequest.relations_by_csd(self.url, self.token, rfc, uuid, b64cert, b64key, cPassword)
    
    def RelationsPfx(self, rfc, uuid, b64Pfx, cPassword):
        return RelationsRequest.relations_by_pfx(self.url, self.token, rfc, uuid, b64Pfx, cPassword)

    def RelationsUuid(self, rfc, uuid):
        return RelationsRequest.relations_by_uuid(self.url, self.token, rfc, uuid)