from Csd.csd_request import CsdRequest
from Utils.services import Services

class Csd(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Csd, self).__init__(url, token, user, password)

    def upload_csd(self, certificate_type, b64_cert, b64_key, password):
        return CsdRequest.upload_csd(self.get_url(), self.get_token(), certificate_type, b64_cert, b64_key, password)
