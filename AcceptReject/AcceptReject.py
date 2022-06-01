from AcceptReject.AcceptRejectRequest import AcceptRejectRequest
from Utils.Services import Services

class AcceptReject(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(AcceptReject, self).__init__(url, token, user, password)
    
    def accept_reject_xml(self, xml_cancel):
        return AcceptRejectRequest.accept_reject_xml(self.get_url(), self.get_token(), xml_cancel)

    def accept_reject_csd(self, rfc, uuids, b64_cert, b64_key, password):
        return AcceptRejectRequest.accept_reject_csd(self.get_url(), self.get_token(), rfc, uuids, b64_cert, b64_key, password)
    
    def accept_reject_pfx(self, rfc, uuids, b64_pfx, password):
        return AcceptRejectRequest.accept_reject_pfx(self.get_url(), self.get_token(), rfc, uuids, b64_pfx, password)

    def accept_reject_uuid(self, rfc, uuid, accion):
        return AcceptRejectRequest.accept_reject_uuid(self.get_url(), self.get_token(), rfc, uuid, accion)