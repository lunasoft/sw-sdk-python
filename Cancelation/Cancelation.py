from cancelation.cancelation_request import CancelationRequest
from utils.services import Services

class Cancelation(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Cancelation, self).__init__(url, token, user, password)
    
    def cancel_xml(self, xml_cancel):
        return CancelationRequest.cancel_xml(self.url, self.token, xml_cancel)

    def cancel_csd(self, rfc, uuid, b64_cert, b64_key, password):
        return CancelationRequest.cancel_csd(self.url, self.token, rfc, uuid, b64_cert, b64_key, password)
    
    def cancel_pfx(self, rfc, uuid, b64_pfx, password):
        return CancelationRequest.cancel_pfx(self.url, self.token, rfc, uuid, b64_pfx, password)

    def cancel_uuid(self, rfc, uuid):
        return CancelationRequest.cancel_uuid(self.url, self.token, rfc, uuid)