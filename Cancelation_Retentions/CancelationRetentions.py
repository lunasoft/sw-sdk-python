from Cancelation_Retentions.CancelationRetentionsRequest import CancelationRetentionsRequest
from Utils.Services import Services

class CancelationRetentions(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(CancelationRetentions, self).__init__(url, token, user, password)
    
    def CancelaUno(self, xmlCancel):
        return CancelationRetentionsRequest.cancel_by_xml(self.get_url(), self.get_token(), xmlCancel)

    def CancelaUnoCSD(self, uuid, rfc, b64cert, b64key, cPassword, motivo, foliosustitucion):
        return CancelationRetentionsRequest.cancel_by_csd(self.get_url(), self.get_token(), uuid, rfc, b64cert, b64key, cPassword, motivo, foliosustitucion)
    
    def CancelaUnoPFX(self, uuid, rfc, b64Pfx, cPassword, motivo, foliosustitucion):
        return CancelationRetentionsRequest.cancel_by_pfx(self.get_url(), self.get_token(), uuid, rfc, b64Pfx, cPassword, motivo, foliosustitucion)
