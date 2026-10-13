from StampRetentions.StampRetentionsRequest import StampRetentionsRequest
from Utils.Services import Services

class StampRetentions(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(StampRetentions, self).__init__(url, token, user, password)
    
    def stamp_retentions_v3(self, xml):
        return StampRetentionsRequest.stamp(self.get_url(), self.get_token(), xml, "/retencion/stamp/v3")


