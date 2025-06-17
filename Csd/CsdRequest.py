from Csd.CsdResponse import CsdResponse
from Utils.requestHelper import RequestHelper

class CsdRequest:    
    @staticmethod
    def upload_csd(url, token, certificate_type, b64_cert, b64_key, password):
        payload = { 
                   "password": password, 
                   "type": certificate_type, 
                   "b64Cer": b64_cert, 
                   "b64Key": b64_key 
                   }
        endpoint = url + "/certificates/save"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return CsdResponse(response)