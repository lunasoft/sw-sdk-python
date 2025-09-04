from Stamp_Retentions.Stamp_RetentionsResponse import Stamp_RetentionsResponse
from Utils.requestHelper import RequestHelper

class Stamp_RetentionsRequest:
    @staticmethod
    def stamp(url, token, xml, path):
        endpoint = url + path
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return Stamp_RetentionsResponse(response)


