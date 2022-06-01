import requests
import string
import random
from Csd.CsdResponse import CsdResponse

class CsdRequest:
    @staticmethod
    def upload_csd(url, token, certificate_type, b64_cert, b64_key, password):
        payload = "{ \"password\": \"" + password + "\", \"type\": \"" + certificate_type + "\", \"b64Cer\": \"" + b64_cert + "\",  \"b64Key\": \"" + b64_key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/certificates/save", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return CsdResponse(response)