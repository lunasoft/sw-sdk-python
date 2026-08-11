from Csd.CsdRequest import CsdRequest
from Utils.Services import Services

class Csd(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Csd, self).__init__(url, token, user, password)

    def upload_csd(self, certificate_type, b64_cert, b64_key, password):
        return CsdRequest.upload_csd(self.get_url(), self.get_token(), certificate_type, b64_cert, b64_key, password)

    def get_list_csd(self):
        """Consulta todos los certificados de la cuenta (equivalente a GetListCsd en .NET)."""
        return CsdRequest.get_list_csd(self.get_url(), self.get_token())

    def get_csd(self, certificate_number):
        """Consulta un certificado por su número de certificado (equivalente a SearchMyCsd en .NET)."""
        return CsdRequest.get_csd(self.get_url(), self.get_token(), certificate_number)

    def get_list_csd_by_rfc(self, rfc):
        """Consulta los certificados de un RFC (equivalente a GetListCsdByRfc en .NET)."""
        return CsdRequest.get_list_csd_by_rfc(self.get_url(), self.get_token(), rfc)

    def disable_csd(self, certificate_number):
        """Desactiva un certificado por su número de certificado (equivalente a DisableMyCsd en .NET)."""
        return CsdRequest.disable_csd(self.get_url(), self.get_token(), certificate_number)

    def get_list_csd_by_type(self, certificate_type):
        """Consulta los certificados de un tipo (equivalente a GetListCsdByType en .NET)."""
        return CsdRequest.get_list_csd_by_type(self.get_url(), self.get_token(), certificate_type)

    def get_active_csd(self, rfc, certificate_type):
        """Consulta el certificado activo de un RFC por tipo (equivalente a SearchActiveCsd en .NET)."""
        return CsdRequest.get_active_csd(self.get_url(), self.get_token(), rfc, certificate_type)
