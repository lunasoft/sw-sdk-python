from Cancelation.CancelationRequest import CancelationRequest
from Utils.Services import Services

class Cancelation(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Cancelation,self).__init__(url, token, user, password)
    
    def CancelXml(self, xmlCancel):
        return CancelationRequest.cancel_by_xml(self.url, self.token, xmlCancel)

    def CancelCsd(self, rfc, uuid, b64cert, b64key, cPassword):
        return CancelationRequest.cancel_by_csd(self.url, self.token, rfc, uuid, b64cert, b64key, cPassword)
    
    def CancelPfx(self, rfc, uuid, b64Pfx, cPassword):
        return CancelationRequest.cancel_by_pfx(self.url, self.token, rfc, uuid, b64Pfx, cPassword)

    def CancelUuid(self, rfc, uuid):
        return CancelationRequest.cancel_by_uuid(self.url, self.token, rfc, uuid)