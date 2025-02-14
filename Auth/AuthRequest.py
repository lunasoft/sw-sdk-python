from Auth.AuthResponse import AuthResponse
from Utils.requestHelper import RequestHelper

class AuthRequest:
    @staticmethod
    def authenticate(url, user, password):
        payload = {'user': user, 'password': password}
        headers = {'Content-Type': 'application/json', 'Cache-Control': "no-cache"}
        endpoint = url + "/v2/security/authenticate"
        response = RequestHelper.post_json_request_Without_Headers(endpoint,payload, headers)
        return AuthResponse(response)