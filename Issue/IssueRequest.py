import requests
import string
import random
from Issue.issue_response import IssueResponse

class IssueRequest:
    @staticmethod
    def issue(url, token, xml, path, base64=False):
        bs64 = ""
        if base64:
            bs64 = "/b64"
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xml) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\""
        }
        response = requests.request("POST", url + path + bs64, data = payload.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return IssueResponse(response)
    @staticmethod
    def issue_json(url, token, json, version):
        if(isinstance(json, dict)):
            json = json.dumps(json)
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/jsontoxml"
        }
        response = requests.request("POST", url + "/v3/cfdi33/issue/json/" + version, data = json.encode('utf-8'), headers = headers, verify = True, timeout = 300)
        return IssueResponse(response)