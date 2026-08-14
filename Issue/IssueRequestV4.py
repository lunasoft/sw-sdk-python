from Utils.requestHelper import RequestHelper
from Issue.IssueResponse import IssueResponse
from Utils.response_version import ResponseVersion
from typing import Optional, Dict, Union

class IssueRequestV4:
    @staticmethod
    def _build_headers(headers: Optional[Dict], email, custom_id: str, pdf: bool) -> Dict:
        request_headers = {}
        if email:
            request_headers['email'] = ",".join(email) if isinstance(email, list) else email
        if custom_id:
            request_headers['customid'] = custom_id
        if pdf:
            request_headers['extra'] = "pdf"
        if headers:
            request_headers.update(headers)
        return request_headers

    @staticmethod
    def issue_xml(url: str, token: str, xml: str, headers: Optional[Dict], version: ResponseVersion,
                  email=None, custom_id: str = None, pdf: bool = False, b64: bool = False) -> IssueResponse:
        bs64 = "/b64" if b64 else ""
        path = f"/v4/cfdi33/issue/{str(version)}{bs64}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4(
            endpoint=complete_url,
            content=xml,
            token=token,
            headers=IssueRequestV4._build_headers(headers, email, custom_id, pdf)
        )
        return IssueResponse(response)

    @staticmethod
    def issue_json(url: str, token: str, json_data: Union[str, dict], headers: Optional[Dict], version: ResponseVersion,
                   email=None, custom_id: str = None, pdf: bool = False) -> IssueResponse:
        path = f"/v4/cfdi33/issue/json/{str(version)}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4_json(
            endpoint=complete_url,
            content=json_data,
            token=token,
            headers=IssueRequestV4._build_headers(headers, email, custom_id, pdf)
        )
        return IssueResponse(response)
