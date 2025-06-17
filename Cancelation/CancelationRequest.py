from Cancelation.CancelationResponse import CancelationResponse
from Utils.requestHelper import RequestHelper

class CancelationRequest:    
    @staticmethod
    def cancel_by_xml(url, token, xml_cancelacion):
        endpoint = url + "/cfdi33/cancel/xml"
        response = RequestHelper.post_multipart_request(endpoint, token, xml_cancelacion)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_csd(url, token, rfc, uuid, b64cert, b64key, password, motivo, foliosustitucion):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "motivo": motivo,
            "foliosustitucion": foliosustitucion,
            "b64Cer": b64cert,
            "b64Key": b64key
        }
        endpoint = url + "/cfdi33/cancel/csd"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_pfx(url, token, rfc, uuid, b64Pfx, password, motivo, foliosustitucion):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "motivo": motivo,
            "foliosustitucion": foliosustitucion,
            "b64Pfx": b64Pfx
        }
        endpoint = url + "/cfdi33/cancel/pfx"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return CancelationResponse(response)

    @staticmethod
    def cancel_by_uuid(url, token, rfc, uuid, motivo, foliosustitucion):
        endpoint = f"{url}/cfdi33/cancel/{rfc}/{uuid}/{motivo}/{foliosustitucion}"
        response = RequestHelper.post_json_request(endpoint,token, None)
        return CancelationResponse(response)