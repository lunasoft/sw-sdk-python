from Cancelation_Retentions.CancelationRetentionsResponse import CancelationRetentionsResponse
from Utils.requestHelper import RequestHelper

class CancelationRetentionsRequest:    
    @staticmethod
    def cancel_by_xml(url, token, xml_cancelacion):
        endpoint = url + "/retencion/cancel/xml"
        response = RequestHelper.post_multipart_request(endpoint, token, xml_cancelacion)
        return CancelationRetentionsResponse(response)

    @staticmethod
    def cancel_by_csd(url, token, uuid, rfc, b64cert, b64key, password, motivo, foliosustitucion):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "motivo": motivo,
            "foliosustitucion": foliosustitucion,
            "b64Cer": b64cert,
            "b64Key": b64key
        }
        endpoint = url + "/retencion/cancel/csd"
        response = RequestHelper.post_json_request(endpoint, token, payload)
        return CancelationRetentionsResponse(response)

    @staticmethod
    def cancel_by_pfx(url, token, uuid, rfc, b64Pfx, password, motivo, foliosustitucion):
        payload = {
            "uuid": uuid,
            "password": password,
            "rfc": rfc,
            "motivo": motivo,
            "foliosustitucion": foliosustitucion,
            "b64Pfx": b64Pfx
        }
        endpoint = url + "/retencion/cancel/pfx"
        response = RequestHelper.post_json_request(endpoint, token, payload)
        return CancelationRetentionsResponse(response)
