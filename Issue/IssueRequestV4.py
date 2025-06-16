from Utils.requestHelper import RequestHelper
from Issue.IssueResponse import IssueResponse
from Utils.response_version import ResponseVersion
from typing import Optional, Dict, Union

class IssueRequestV4:
    @staticmethod
   
    def issue_xml(url: str, token: str, xml: str, headers: Optional[Dict], version: ResponseVersion) -> IssueResponse:
        """ Método estático para timbrar usando el servicio Emisión Timbrado XML V4 con soporte de versiones de respuesta."""
        path = f"/v4/cfdi33/issue/{str(version)}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4(
            endpoint=complete_url,
            content=xml,
            token=token,
            headers=headers
        )
        return IssueResponse(response)

    @staticmethod
    def issue_json(url: str, token: str, json_data: Union[str, dict], headers: Optional[Dict], version: ResponseVersion) -> IssueResponse:
        """" Método estático para timbrar usando el servicio Emisión Timbrado JSON V4 con soporte de versiones de respuesta."""
        path = f"/v4/cfdi33/issue/json/{str(version)}"
        complete_url = f"{url}{path}"
        response = RequestHelper.post_v4_json(
            endpoint=complete_url,
            content=json_data,
            token=token,
            headers=headers
        )
        return IssueResponse(response)
