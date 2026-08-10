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
    def _validate_required(value, message):
        """Valida que un parámetro obligatorio no venga en None ni vacío.
        Lanza ValueError antes de armar el endpoint y de ejecutar la petición."""
        if value is None or not str(value).strip():
            raise ValueError(message)

    @staticmethod
    def get_list_csd(url, token):
        """Consulta todos los certificados de la cuenta asociada al token."""
        endpoint = url + "/certificates"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_csd(url, token, certificate_number):
        """Consulta un certificado por su número de certificado."""
        CsdRequest._validate_required(certificate_number, "Debe especificar el número de certificado")
        endpoint = f"{url}/certificates/{certificate_number}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def get_list_csd_by_rfc(url, token, rfc):
        """Consulta los certificados de la cuenta que pertenecen a un RFC."""
        CsdRequest._validate_required(rfc, "Debe especificar el RFC")
        endpoint = f"{url}/certificates/rfc/{rfc}"
        response = RequestHelper.get_json_request(endpoint,token)
        return CsdResponse(response)

    @staticmethod
    def disable_csd(url, token, certificate_number):
        """Desactiva (elimina) un certificado por su número de certificado."""
        CsdRequest._validate_required(certificate_number, "Debe especificar el número de certificado")
        endpoint = f"{url}/certificates/{certificate_number}"
        response = RequestHelper.delete_json_request(endpoint,token)
        return CsdResponse(response)
