import json
from Issue.IssueResponse import IssueResponse
from Utils.requestHelper import RequestHelper

class IssueRequest:
    @staticmethod
    def issue(url, token, xml, path, base64=False):
        bs64 = ""
        if base64:
            bs64 = "/b64"
        endpoint = url + path + bs64
        response = RequestHelper.post_multipart_request(endpoint, token, xml)
        return IssueResponse(response)
    
    @staticmethod
    def issue_json(url, token, json, version):
        if(isinstance(json, dict)):
            json = json.dumps(json)
        endpoint = url + "/v3/cfdi33/issue/json/" + version
        response = RequestHelper.post_jsontoxml_request(endpoint,token,json)
        return IssueResponse(response)