from Stamp.StampResponse import StampResponse
from Utils.requestHelper import RequestHelper

class StampRequest:
    @staticmethod
    def stamp(url, token, xml, path, base64 = False):
        bs64 = ""
        if base64:
            bs64 = "/b64"

        endpoint = url + path + bs64
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return StampResponse(response)