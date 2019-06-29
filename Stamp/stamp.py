from Stamp.stamp_request import StampRequest
from Utils.services import Services

class Stamp(Services):
    def __init__(self, url, token, user = None, password = None):
        super(Stamp, self).__init__(url, token, user, password)
    
    def stamp_v1(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/stamp/v1", b64)
    def stamp_v2(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/stamp/v2", b64)
    def stamp_v3(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/stamp/v3", b64)
    def stamp_v4(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/stamp/v4", b64)
    def stamp_version2_v1(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/v2/stamp/v1", b64)
    def stamp_version2_v2(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/v2/stamp/v2", b64)
    def stamp_version2_v3(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/v2/stamp/v3", b64)
    def stamp_version2_v4(self, xml, b64 = False):
        return StampRequest.stamp(self.get_url(), self.get_token(), xml, "/cfdi33/v2/stamp/v4", b64)
