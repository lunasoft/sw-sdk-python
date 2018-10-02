from AcceptReject.AcceptRejectRequest import AcceptRejectRequest
from Utils.Services import Services

class AcceptReject(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(AcceptReject,self).__init__(url, token, user, password)
    
    def AcceptRejectXml(self, xmlCancel):
        return AcceptRejectRequest.AcceptReject_by_xml(self.url, self.token, xmlCancel)

    def AcceptRejectCsd(self, rfc, uuids, b64cert, b64key, cPassword):
        return AcceptRejectRequest.AcceptReject_by_csd(self.url, self.token, rfc, uuids, b64cert, b64key, cPassword)
    
    def AcceptRejectPfx(self, rfc, uuids, b64Pfx, cPassword):
        return AcceptRejectRequest.AcceptReject_by_pfx(self.url, self.token, rfc, uuids, b64Pfx, cPassword)

    def AcceptRejectUuid(self, rfc, uuid):
        return AcceptRejectRequest.AcceptReject_by_uuid(self.url, self.token, rfc, uuid)