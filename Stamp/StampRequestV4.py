from Utils.requestHelper import RequestHelper
from Stamp.StampResponse import StampResponse
from Utils.response_version import ResponseVersion

class StampRequestV4:
    @staticmethod
    def _build_headers(headers: dict, email, custom_id: str, pdf: bool) -> dict:
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
    def stamp(url: str, token: str, xml: str, headers: dict, version: ResponseVersion,
              email=None, custom_id: str = None, pdf: bool = False, b64: bool = False):
        bs64 = "/b64" if b64 else ""
        path = f"/v4/cfdi33/stamp/{str(version)}{bs64}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4(
            endpoint=complete_url,
            content=xml,
            token=token,
            headers=StampRequestV4._build_headers(headers, email, custom_id, pdf)
        )
        return StampResponse(response)
