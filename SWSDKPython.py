import requests


class SWSDKPython:

    @staticmethod
    def authenticate(url, user, password):
        headers = {'user': user, 'password': password, 'Cache-Control': "no-cache"}
        response = requests.request("POST", url + "/security/authenticate", headers=headers)
        return response.text

    @staticmethod
    def stamp(url, token, xml, version, b64=False):
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
        response = requests.request("POST", url + "/cfdi33/stamp/" + version + "/" + bs64, data=payload,
                                    headers=headers)
        return response.text

    @staticmethod
    def issue(url, token, xml, version, b64=False):
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

    @staticmethod
    def cancel_by_xml(url, token, xmlCancelacion):
        boundary = "----=_Part_11_11939969.1490230712432"
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: " \
                                    "form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(
            xmlCancelacion) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + "/cfdi33/cancel/xml", data=payload, headers=headers)
        return response.text

    @staticmethod
    def cancel_by_csd(url, token, rfc, uuid, b64cert, b64key, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\"," \
                                                                                 "  \"rfc\": \"" + rfc + "\",    \"b64Cer\": \"" + b64cert + "\",  \"b64Key\": \"" + b64key + "\"}"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/csd", data=payload, headers=headers)
        return response.text

    @staticmethod
    def cancel_by_pfx(url, token, rfc, uuid, b64Pfx, password):
        payload = "{ \"uuid\": \"" + uuid + "\",  \"password\": \"" + password + "\"," \
                                                                                 "  \"rfc\": \"" + rfc + "\",    \"b64Pfx\": \"" + b64Pfx + "\" }"
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/pfx", data=payload, headers=headers)
        return response.text

    @staticmethod
    def cancel_by_uuid(url, token, rfc, uuid):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url + "/cfdi33/cancel/" + rfc + "/" + uuid, headers=headers)
        return response.text

    @staticmethod
    def validate_lrfc(url, token, lrfc):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/lrfc/" + lrfc, headers=headers)
        return response.text

    @staticmethod
    def validate_lco(url, token, lco):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/lco/" + lco, headers=headers)
        return response.text

    @staticmethod
    def account_balance(url, token):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/account/balance", headers=headers)
        return response.text

    @staticmethod
    def validate(url, token, xml, b64=False):
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
        response = requests.request("POST", url + "/validate/cfdi33/" + bs64, data=payload,
                                    headers=headers)
        return response.text

    def generate_token(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password

        if self.user is None or self.password is None:
            raise Exception('Hace falta el usuario y/o contraseña')
        headers = {'user': self.user, 'password': self.password, 'Cache-Control': "no-cache"}
        response = requests.request("POST", self.uri + "/security/authenticate", headers=headers)
        return response
