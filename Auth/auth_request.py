import requests
from Auth.auth_response import AuthResponse
class AuthRequest:
    @staticmethod
    def authenticate(url, user, password):
        headers = {'user': user, 'password': password, 'Cache-Control': "no-cache"}
        response = requests.request("POST", (url + "/security/authenticate"), headers = headers, verify = True, timeout = 300)
        response_obj = AuthResponse(response)
        return response_obj