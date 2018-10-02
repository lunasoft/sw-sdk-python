from Stamp.StampRequest import StampRequest
from Utils.Services import Services

class Stamp(Services):
    def __init__(self, url, token, user=None, password=None):
        super(Stamp,self).__init__(url, token, user, password)
    
    def StampV1(self,xml,b64=False):
        return StampRequest.stamp(self.url, self.token, xml, "v1", b64)
    def StampV2(self,xml,b64=False):
        return StampRequest.stamp(self.url, self.token, xml, "v2", b64)
    def StampV3(self,xml,b64=False):
        return StampRequest.stamp(self.url, self.token, xml, "v3", b64)
    def StampV4(self,xml,b64=False):
        return StampRequest.stamp(self.url, self.token, xml, "v4", b64)