from Relations.RelationsResponse import RelationsResponse
from Utils.requestHelper import RequestHelper

class RelationsRequest:
    @staticmethod
    def relations_csd(url, token, rfc, uuid, b64_cert, b64_key, password):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "b64Cer": b64_cert,
            "b64Key": b64_key
        }
        endpoint = url + "/relations/csd"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return RelationsResponse(response)

    @staticmethod
    def relations_pfx(url, token, rfc, uuid, b64_pfx, password):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "b64Pfx": b64_pfx
        }
        endpoint = url + "/relations/pfx"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return RelationsResponse(response)

    @staticmethod
    def relations_uuid(url, token, rfc, uuid):
        endpoint = url + "/relations/" + rfc + "/" + uuid
        response = RequestHelper.post_json_request(endpoint,token,None)
        return RelationsResponse(response)