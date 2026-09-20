from Cancelation.CancelationRequest import CancelationRequest
from Utils.Services import Services

class Cancelation(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Cancelation, self).__init__(url, token, user, password)
    
    def CancelXml(self, xmlCancel):
        return CancelationRequest.cancel_by_xml(self.get_url(), self.get_token(), xmlCancel)

    def CancelCsd(self, uuid, rfc, b64cert, b64key, cPassword, motivo, foliosustitucion):
        return CancelationRequest.cancel_by_csd(self.get_url(), self.get_token(), rfc, uuid, b64cert, b64key, cPassword, motivo, foliosustitucion)
    
    def CancelPfx(self, uuid, rfc, b64Pfx, cPassword, motivo, foliosustitucion):
        return CancelationRequest.cancel_by_pfx(self.get_url(), self.get_token(), rfc, uuid, b64Pfx, cPassword, motivo, foliosustitucion)

    def CancelUuid(self, rfc, uuid, motivo, foliosustitucion):
        return CancelationRequest.cancel_by_uuid(self.get_url(), self.get_token(), rfc, uuid, motivo, foliosustitucion)
