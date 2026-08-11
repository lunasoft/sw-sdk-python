from Csd.CsdResponse import CsdResponse
from Utils.requestHelper import RequestHelper

class CsdRequest:    
    @staticmethod
    def upload_csd(url, token, certificate_type, b64_cert, b64_key, password):
        payload = { 
                   "password": password, 
                   "type": certificate_type, 
                   "b64Cer": b64_cert, 
                   "b64Key": b64_key 
                   }
        endpoint = url + "/certificates/save"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return CsdResponse(response)

    @staticmethod
    def get_list_csd(url, token):
        """Consulta todos los certificados de la cuenta asociada al token."""
        endpoint = url + "/certificates"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_csd(url, token, certificate_number):
        """Consulta un certificado por su número de certificado."""
        endpoint = f"{url}/certificates/{certificate_number}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_list_csd_by_rfc(url, token, rfc):
        """Consulta los certificados de la cuenta que pertenecen a un RFC."""
        endpoint = f"{url}/certificates/rfc/{rfc}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def disable_csd(url, token, certificate_number):
        """Desactiva (elimina) un certificado por su número de certificado."""
        endpoint = f"{url}/certificates/{certificate_number}"
        response = RequestHelper.delete_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_list_csd_by_type(url, token, certificate_type):
        """Consulta los certificados de la cuenta que son de un tipo (stamp o fiel)."""
        endpoint = f"{url}/certificates/type/{certificate_type}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_active_csd(url, token, rfc, certificate_type):
        """Consulta el certificado activo de un RFC para un tipo (stamp o fiel)."""
        endpoint = f"{url}/certificates/rfc/{rfc}/{certificate_type}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)
