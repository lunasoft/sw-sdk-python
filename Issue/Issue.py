from issue.issue_request import IssueRequest
from utils.services import Services

class Issue(Services):
    def __init__(self, url, token, user=None, password=None):
        super(Issue, self).__init__(url, token, user, password)
    
    def issue_v1(self, xml, b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v1", b64)
    def issue_v2(self, xml, b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v2", b64)
    def issue_v3(self, xml, b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v3", b64)
    def issue_v4(self, xml, b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v4", b64)
    def issue_json_v1(self, json):
        return IssueRequest.issue_json(self.url, self.token, json, "v1")
    def issue_json_v2(self, json):
        return IssueRequest.issue_json(self.url, self.token, json, "v2")
    def issue_json_v3(self, json):
        return IssueRequest.issue_json(self.url, self.token, json, "v3")
    def issue_json_v4(self, json):
        return IssueRequest.issue_json(self.url, self.token, json, "v4")