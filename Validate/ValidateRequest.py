from Validate.ValidateResponse import ValidateResponse
from Utils.requestHelper import RequestHelper

class ValidateRequest:
    @staticmethod
    def validate_xml(url, token, xml, status=None):
        path = ''
        if status == True or status==None:
            path = "/cfdi"
        elif status == False:
            path = "/cfdi?validatestatus=false"
        endpoint = url + "/validate" + path
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return ValidateResponse(response)