from StampRetentions.StampRetentionsResponse import StampRetentionsResponse
from Utils.requestHelper import RequestHelper

class StampRetentionsRequest:
    @staticmethod
    def stamp(url, token, xml, path):
        endpoint = url + path
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return StampRetentionsResponse(response)


