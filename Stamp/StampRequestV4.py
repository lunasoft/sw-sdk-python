from Utils.requestHelper import RequestHelper
from Stamp.StampResponse import StampResponse
from Utils.response_version import ResponseVersion

class StampRequestV4:
    @staticmethod
    def stamp(url: str, token: str, xml: str, headers: dict, version: ResponseVersion):
        """
        Método estático para timbrar usando el servicio Timbrado v4 con soporte de versiones de respuesta.
        """
        path = f"/v4/cfdi33/stamp/{str(version)}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4(
            endpoint=complete_url,
            content=xml,
            token=token,
            headers=headers
        )
        return StampResponse(response)
