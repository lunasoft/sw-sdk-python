import requests
import string
import random
import json
from AcceptReject.AcceptRejectResponse import AcceptRejectResponse

class AcceptRejectRequest:
    @staticmethod
    def AcceptReject_by_xml(url, token, xmlCancelacion):
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xmlCancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/acceptreject/xml", data=payload, headers=headers)
        return AcceptRejectResponse(response)

    @staticmethod
    def AcceptReject_by_csd(url, token, rfc, uuids, b64cert, b64key, password):
        uuid = json.dumps(uuids)
        payload = "{ \"uuids\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64cert + "\",  \"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/csd", data=payload, headers=headers)
        return AcceptRejectResponse(response)

    @staticmethod
    def AcceptReject_by_pfx(url, token, rfc, uuids, b64Pfx, password):
        uuid = json.dumps(uuids)
        payload = "{ \"uuids\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/pfx", data=payload, headers=headers)
        return AcceptRejectResponse(response)

    @staticmethod
    def AcceptReject_by_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/" + rfc + "/" + uuid, headers=headers)
        return AcceptRejectResponse(response)