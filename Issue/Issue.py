from Issue.IssueRequest import IssueRequest
from Utils.Services import Services

class Issue(Services):
    def __init__(self, url, token, user=None, password=None):
        super(Issue,self).__init__(url, token, user, password)
    
    def IssueV1(self,xml,b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v1", b64)
    def IssueV2(self,xml,b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v2", b64)
    def IssueV3(self,xml,b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v3", b64)
    def IssueV4(self,xml,b64=False):
        return IssueRequest.issue(self.url, self.token, xml, "v4", b64)