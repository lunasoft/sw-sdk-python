import requests
import random
import string
import json
from typing import Union, Dict

class RequestHelper:
    @staticmethod
    def _get_session():
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount("https://", adapter)
        return session

    @staticmethod
    def post_json_request_Without_Headers(endpoint, payload, headers=None):
        session = RequestHelper._get_session()
        return session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)

    @staticmethod
    def post_json_request(endpoint, token, payload=None):
        headers = {
            'Authorization': f"bearer {token}",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        session = RequestHelper._get_session()
        return session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)

    @staticmethod
    def post_jsontoxml_request(endpoint, token, payload=None):
        headers = {
            'Authorization': f"bearer {token}",
            'Content-Type': "application/jsontoxml; charset=utf-8",
            'Cache-Control': "no-cache"
        }
        session = RequestHelper._get_session()
        return session.post(endpoint, data=payload.encode('utf-8'), headers=headers, verify=True, timeout=300)

    @staticmethod
    def get_json_request(endpoint, token, payload=None):
        headers = {
            'Authorization': f"bearer {token}",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        session = RequestHelper._get_session()
        return session.get(endpoint, json=payload, headers=headers, verify=True, timeout=300)

    @staticmethod
    def delete_json_request(endpoint, token, payload=None):
        headers = {
            'Authorization': f"bearer {token}",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        session = RequestHelper._get_session()
        return session.delete(endpoint, json=payload, headers=headers, verify=True, timeout=300)

    @staticmethod
    def put_json_request(endpoint, token, payload=None):
        headers = {
            'Authorization': f"bearer {token}",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        session = RequestHelper._get_session()
        return session.put(endpoint, json=payload, headers=headers, verify=True, timeout=300)

    @staticmethod
    def post_multipart_request(endpoint, token, xml_data):
        boundary = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        body = RequestHelper._create_multipart_body(xml_data, boundary)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
        session = RequestHelper._get_session()
        return session.post(endpoint, data=body, headers=headers, verify=True, timeout=300)

    @staticmethod
    def _create_multipart_body(content: Union[str, dict], boundary: str) -> bytes:
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        body = (
            f"--{boundary}\r\n"
            "Content-Type: text/xml\r\n"
            "Content-Transfer-Encoding: binary\r\n"
            'Content-Disposition: form-data; name="xml"; filename="xml"\r\n\r\n'
            f"{str(content)}\r\n"
            f"--{boundary}--"
        )
        return body.encode('utf-8')

    @staticmethod
    def post_v4_json(endpoint: str, content: Union[str, dict], token: str = None, headers: Dict = None) -> requests.Response:
        request_headers = {
            'Authorization': f'Bearer {token}' if token else None,
            'Content-Type': 'application/jsontoxml; charset=utf-8'
        }
        if headers:
            request_headers.update(headers)
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        return requests.post(endpoint, data=content.encode('utf-8'), headers=request_headers)

    @staticmethod
    def post_v4(endpoint: str, content: Union[str, dict], token: str = None, headers: Dict = None) -> requests.Response:
        request_headers = {
            'Authorization': f'Bearer {token}' if token else None
        }
        if headers:
            request_headers.update(headers)
        boundary = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        request_headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        body = RequestHelper._create_multipart_body(content, boundary)
        return requests.post(endpoint, data=body, headers=request_headers)
