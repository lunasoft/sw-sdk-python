from typing import Optional, Dict, Union
from Utils.Services import Services
from Issue.IssueRequestV4 import IssueRequestV4
from Utils.response_version import ResponseVersion
from Issue.IssueResponse import IssueResponse

class IssueV4(Services):
    def __init__(self, url: str, token: str = None, user: str = None, password: str = None):
        super(IssueV4, self).__init__(url, token, user, password)

    def issue_xml(self, xml: str, headers: Optional[Dict] = None, version: ResponseVersion = ResponseVersion.V1) -> IssueResponse:
        return IssueRequestV4.issue_xml(
            url=self.get_url(),
            token=self.get_token(),
            xml=xml,
            headers=headers,
            version=version
        )

    def issue_json(self, json_data: Union[str, dict], headers: Optional[Dict] = None, version: ResponseVersion = ResponseVersion.V1) -> IssueResponse:
        return IssueRequestV4.issue_json(
            url=self.get_url(),
            token=self.get_token(),
            json_data=json_data,
            headers=headers,
            version=version
        )
