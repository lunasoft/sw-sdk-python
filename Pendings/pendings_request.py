import requests
from Pendings.pendings_response import PendingsResponse
class PendingsRequest:
    @staticmethod
    def pendings_rfc(url, token, rfc):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/pendings/" + rfc, headers = headers, verify = True, timeout = 300)
        return PendingsResponse(response)