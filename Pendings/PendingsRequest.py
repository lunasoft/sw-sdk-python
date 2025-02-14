from Pendings.PendingsResponse import PendingsResponse
from Utils.requestHelper import RequestHelper

class PendingsRequest:
    @staticmethod
    def pendings_rfc(url, token, rfc):
        endpoint = url + "/pendings/" + rfc
        response = RequestHelper.get_json_request(endpoint,token,None)
        return PendingsResponse(response)