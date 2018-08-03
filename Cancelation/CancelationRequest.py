import requests
from Cancelation.CancelationResponse import CancelationResponse

class CancelationRequest:
    @staticmethod
    def cancel_by_xml(url, token, xmlCancelacion):
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xmlCancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/cancel/xml", data=payload, headers=headers)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_csd(url, token, rfc, uuid, b64cert, b64key, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64cert + "\",  \"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/csd", data=payload, headers=headers)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_pfx(url, token, rfc, uuid, b64Pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\", \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/pfx", data=payload, headers=headers)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/" + rfc + "/" + uuid, headers=headers)
        return CancelationResponse(response)