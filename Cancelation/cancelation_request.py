import requests
import string
import random
from Cancelation.cancelation_response import CancelationResponse

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
        response = requests.request("POST", url + "/cfdi33/cancel/xml", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod

    def cancel_by_csd(url, token, rfc, uuid, b64cert, b64key, password, motivo, foliosustitucion):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\", \"motivo\": \"" + motivo + "\", \"foliosustitucion\": \"" + foliosustitucion + "\",\"b64Cer\": \"" + b64cert + "\",\"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/csd", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod

    def cancel_by_pfx(url, token, rfc, uuid, b64Pfx, password, motivo, foliosustitucion):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc  + "\", \"motivo\": \"" + motivo + "\", \"foliosustitucion\": \"" + foliosustitucion + "\",\"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/pfx", data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)

    @staticmethod

    def cancel_by_uuid(url, token, rfc, uuid, motivo, foliosustitucion):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }

        response = requests.request("POST", url + "/cfdi33/cancel/" + rfc + "/" + uuid + "/" + motivo + "/" + foliosustitucion , headers = headers, verify = True, timeout = 300)
        return CancelationResponse(response)