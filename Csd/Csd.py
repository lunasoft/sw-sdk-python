from Csd.CsdRequest import CsdRequest
from Utils.Services import Services

class Csd(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Csd, self).__init__(url, token, user, password)

    def upload_csd(self, certificate_type, b64_cert, b64_key, password):
        return CsdRequest.upload_csd(self.get_url(), self.get_token(), certificate_type, b64_cert, b64_key, password)

    def get_list_csd(self):
        return CsdRequest.get_list_csd(self.get_url(), self.get_token())

    def get_csd(self, certificate_number):
        return CsdRequest.get_csd(self.get_url(), self.get_token(), certificate_number)

    def get_list_csd_by_rfc(self, rfc):
        return CsdRequest.get_list_csd_by_rfc(self.get_url(), self.get_token(), rfc)

    def disable_csd(self, certificate_number):
        return CsdRequest.disable_csd(self.get_url(), self.get_token(), certificate_number)

    def get_list_csd_by_type(self, certificate_type):
        return CsdRequest.get_list_csd_by_type(self.get_url(), self.get_token(), certificate_type)

    def get_active_csd(self, rfc, certificate_type):
        return CsdRequest.get_active_csd(self.get_url(), self.get_token(), rfc, certificate_type)
