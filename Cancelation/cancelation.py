from Cancelation.CancelationRequest import CancelationRequest
from Utils.Services import Services

class Cancelation(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Cancelation,self).__init__(url, token, user, password)
    
    def CancelXml(self, xmlCancel):
        return CancelationRequest.cancel_by_xml(self.url, self.token, xmlCancel)

    def CancelCsd(self, uuid, cPassword, rfc, motivo,foliosustitucion, b64cert, b64key):
        return CancelationRequest.cancel_by_csd(self.url, self.token, rfc, uuid, b64cert, b64key, cPassword, motivo, foliosustitucion)
    
    def CancelPfx(self, uuid, cPassword, rfc, motivo, foliosustitucion,  b64Pfx):
        return CancelationRequest.cancel_by_pfx(self.url, self.token, rfc, uuid, b64Pfx, cPassword, motivo, foliosustitucion)

    def CancelUuid(self, rfc, uuid, motivo, foliosustitucion):
        return CancelationRequest.cancel_by_uuid(self.url, self.token, rfc, uuid, motivo, foliosustitucion)