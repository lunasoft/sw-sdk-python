import requests
import string
import random
from Csd.csd_response import CsdResponse

class CsdRequest:
    @staticmethod
    def upload_csd(url, token, is_active, certificate_type, b64_cert, b64_key, password):
        payload = "{ \"is_active\": \"" + is_active + "\",  \"password\": \"" + password + "\", \"certificate_type\": \"" + certificate_type + "\",    \"b64Cer\": \"" + b64_cert + "\",  \"b64Key\": \"" + b64_key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/csd/save", data = payload, headers = headers, verify = True, timeout = 300)
        return CsdResponse(response)