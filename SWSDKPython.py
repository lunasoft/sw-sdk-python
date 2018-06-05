import base64
from idlelib.iomenu import encoding

import requests
import json


class SWSDKPython:

    def authenticate(self, url, user, password):
        headers = {'user': user, 'password': password, 'Cache-Control': "no-cache"}
        response = requests.request("POST", url + "/security/authenticate", headers=headers)
        return response.text

    def stamp(self, url, token, xml, version, b64=False):
        if b64 is True:
            bs64 = "/b64"
        else:
            bs64 = ""
        boundary = "----=_Part_11_11939969.1490230712432"
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: " \
                  "form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xml) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/stamp/" + version + "/" + bs64, data=payload, headers=headers)
        return response.text

    def issue(self, url, token, xml, version, b64=False):
        if b64 is True:
            bs64 = "/b64"
        else:
            bs64 = ""
        boundary = "----=_Part_11_11939969.1490230712432"
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: " \
                  "form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(
            xml) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/issue/" + version + "/" + bs64, data=payload,
                                    headers=headers)
        return response.text

    def cancelByXML(self, url, token, xmlCancelacion):
        boundary = "----=_Part_11_11939969.1490230712432"
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: " \
                  "form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xmlCancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/cancel/xml", data=payload, headers=headers)
        return response.text

    def cancelByCSD(self, url, token, rfc, uuid, b64cert, b64key, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\"," \
                  "  \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64cert + "\",  \"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/csd", data=payload, headers=headers)
        return response.text

    def cancelByPFX(self, url, token, rfc, uuid, b64Pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\"," \
                  "  \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/pfx", data=payload, headers=headers)
        return response.text

    def cancelByUUID(self, url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/" + rfc + "/" + uuid, headers=headers)
        return response.text

    def accountBalance(self, url, token):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/account/balance", headers=headers)
        return response.text

    def validateLRFC(self, url, token, lrfc):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/lrfc/" + lrfc, headers=headers)
        return response.text

    def validateLCO(self, url, token, lco):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/lco/" + lco, headers=headers)
        return response.text


# Prueba
url = "http://services.test.sw.com.mx"
user = "demo"
passwrd = "123456789"

with open("basico.xml", "rb") as xml:
    encoded_string = base64.b64encode(xml.read())


swservice = SWSDKPython()
token = json.loads(swservice.authenticate(url, user, passwrd))
print(token['data']['token'])
rToken = token['data']['token']

timbrar = swservice.stamp(url, rToken, str(encoded_string, encoding), "v4", True)
print(timbrar)
accBalance = swservice.accountBalance(url, token['data']['token'])

print("Estado de cuenta "+accBalance)
