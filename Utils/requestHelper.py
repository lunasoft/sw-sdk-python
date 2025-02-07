import requests
import random
import string

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
        response = session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def post_json_request(endpoint, token, payload=None):
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json"}
        response = session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def get_json_request(endpoint, token, payload=None):
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json"}
        response = session.get(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
        
    @staticmethod
    def post_multipart_request(endpoint,token, xml_data):
        session = RequestHelper._get_session()
        boundary = "".join(random.choices(string.ascii_letters + string.digits, k=30))
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"xml\"; filename=\"xml\"\r\n\r\n" + str(xml_data) + "\r\n--" + boundary + "-- "
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": f'multipart/form-data; boundary="{boundary}"'
        }
        response = session.post(endpoint,data=payload.encode('utf-8'), headers=headers, verify=True, timeout=300)
        return response