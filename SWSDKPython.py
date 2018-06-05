import requests



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

