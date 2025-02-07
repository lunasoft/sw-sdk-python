import json
from AcceptReject.AcceptRejectResponse import AcceptRejectResponse
from Utils.requestHelper import RequestHelper

class AcceptRejectRequest:
    @staticmethod
    def accept_reject_xml(url, token, xml_cancelacion):
        endpoint = url + "/acceptreject/xml"
        response = RequestHelper.post_multipart_request(endpoint, token, xml_cancelacion)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_csd(url, token, rfc, uuids, b64_cert, b64_key, password):
        payload = {
            "uuids": uuids, 
            "password": password,
            "rfc": rfc,
            "b64Cer": b64_cert,
            "b64Key": b64_key
        }
        endpoint = url + "/acceptreject/csd"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_pfx(url, token, rfc, uuids, b64_pfx, password):
        payload = {
            "uuids": uuids, 
            "password": password,
            "rfc": rfc,
            "b64Pfx": b64_pfx
        }
        endpoint = url + "/acceptreject/pfx"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return AcceptRejectResponse(response)

    @staticmethod
    def accept_reject_uuid(url, token, rfc, uuid, accion):
        endpoint = url + "/acceptreject/" + rfc + "/" + uuid + "/" + accion
        response = RequestHelper.post_json_request(endpoint,token,None)
        return AcceptRejectResponse(response)