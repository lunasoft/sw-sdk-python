import requests
import string
import random
from Relations.RelationsResponse import RelationsResponse

class RelationsRequest:
    @staticmethod
    def relations_by_xml(url, token, xmlCancelacion):
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xmlCancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/relations/xml", data=payload, headers=headers)
        return RelationsResponse(response)

    @staticmethod
    def relations_by_csd(url, token, rfc, uuid, b64cert, b64key, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64cert + "\",  \"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/csd", data=payload, headers=headers)
        return RelationsResponse(response)

    @staticmethod
    def relations_by_pfx(url, token, rfc, uuid, b64Pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/pfx", data=payload, headers=headers)
        return RelationsResponse(response)

    @staticmethod
    def relations_by_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/relations/" + rfc + "/" + uuid, headers=headers)
        return RelationsResponse(response)