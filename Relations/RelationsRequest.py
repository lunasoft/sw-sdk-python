import requests
import string
import random
from Relations.RelationsResponse import RelationsResponse

class RelationsRequest:

    @staticmethod
    def relations_csd(url, token, rfc, uuid, b64_cert, b64_key, password, verify = True, timeout = 300):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64_cert + "\",  \"b64Key\": \"" + b64_key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/csd", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return RelationsResponse(response)

    @staticmethod
    def relations_pfx(url, token, rfc, uuid, b64_pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64_pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/pfx", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return RelationsResponse(response)

    @staticmethod
    def relations_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/" + rfc + "/" + uuid, headers = headers, verify = True, timeout = 300)
        return RelationsResponse(response)