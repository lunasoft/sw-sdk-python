import requests
import string
import random
import json
from AcceptReject.accept_reject_response import AcceptRejectResponse

class AcceptRejectRequest:
    @staticmethod
    def accept_reject_xml(url, token, xml_cancelacion):
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xml_cancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/acceptreject/xml", data = payload, headers = headers, verify = True, timeout = 300)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_csd(url, token, rfc, uuids, b64_cert, b64_key, password):
        uuid = json.dumps(uuids)
        payload = "{ \"uuids\": " + uuid + ",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64_cert + "\",  \"b64Key\": \"" + b64_key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/csd", data = payload, headers = headers, verify = True, timeout = 300)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_pfx(url, token, rfc, uuids, b64_pfx, password):
        uuid = json.dumps(uuids)
        payload = "{ \"uuids\": " + uuid + ",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64_pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/pfx", data = payload, headers = headers, verify = True, timeout = 300)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_uuid(url, token, rfc, uuid, accion):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/acceptreject/" + rfc + "/" + uuid + "/" + accion, headers = headers, verify = True, timeout = 300)
        return AcceptRejectResponse(response)