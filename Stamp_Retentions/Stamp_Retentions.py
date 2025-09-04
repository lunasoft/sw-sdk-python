from Stamp_Retentions.Stamp_RetentionsRequest import Stamp_RetentionsRequest
from Utils.Services import Services

class Stamp_Retentions(Services):
    def __init__(self, url, token, user = None, password = None):
        super(Stamp_Retentions, self).__init__(url, token, user, password)
    
    def stamp_retetions_v3(self, xml):
        return Stamp_RetentionsRequest.stamp(self.get_url(), self.get_token(), xml, "/retencion/stamp/v3")


