from Validate.ValidateResponse import ValidateResponse
from Utils.requestHelper import RequestHelper

class ValidateRequest:
    @staticmethod
    def validate_xml(url, token, xml, base64=False):
        bs64 = ""
        if base64:
            bs64 = "/b64"
        endpoint = url + "/validate/cfdi/" + bs64
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return ValidateResponse(response)