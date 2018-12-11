import requests
import string
import random
from cancelation.cancelation_response import CancelationResponse

class CancelationRequest:
    @staticmethod
    def cancel_xml(url, token, xml_cancelacion):
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xml_cancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/cancel/xml", data = payload, headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod
    def cancel_csd(url, token, rfc, uuid, b64_cert, b64_key, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64_cert + "\",  \"b64Key\": \"" + b64_key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/csd", data = payload, headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod
    def cancel_pfx(url, token, rfc, uuid, b64_pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64_pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/pfx", data = payload, headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod
    def cancel_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/" + rfc + "/" + uuid, headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)