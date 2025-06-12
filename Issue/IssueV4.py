from typing import Optional, Dict, Union
from Utils.requestHelper import RequestHelper
from Utils.response_version import ResponseVersion
from Issue.IssueResponse import IssueResponse
from Utils.Services import Services

class IssueV4(Services):
    """Clase para el servicio Issue V4 que soporta versiones de respuesta"""
    
    def __init__(self, url: str, token: str = None, user: str = None, password: str = None):
        """
        Inicializa el servicio Issue V4
        
        Args:
            url: URL base del servicio
            token: Token de autenticación (opcional)
            user: Usuario para autenticación (opcional)
            password: Contraseña para autenticación (opcional)
        """
        super(IssueV4, self).__init__(url, token, user, password)
        
    def issue_xml(self, xml: str, headers: Optional[Dict] = None, version: ResponseVersion = ResponseVersion.V1) -> IssueResponse:
        """
        Timbra un XML usando el servicio V4
        
        Args:
            xml: String del XML a timbrar
            headers: Headers opcionales (customid, email, etc)
            version: Versión de respuesta (default: V1)
            
        Returns:
            IssueResponse: Respuesta del servicio
        """
        endpoint = f"/v4/cfdi33/issue/{str(version)}"
        response = RequestHelper.post_v4(
            url=self.get_url(),
            endpoint=endpoint,
            content=xml,
            token=self.get_token(),
            headers=headers
        )
        return IssueResponse(response)
        
    def issue_json(self, json_data: Union[str, dict], headers: Optional[Dict] = None, version: ResponseVersion = ResponseVersion.V1) -> IssueResponse:
        """
        Timbra un JSON usando el servicio V4
        
        Args:
            json_data: JSON a timbrar (como string o dict)
            headers: Headers opcionales (customid, email, etc)
            version: Versión de respuesta (default: V1)
            
        Returns:
            IssueResponse: Respuesta del servicio
        """
        endpoint = f"/v4/cfdi33/issue/json/{str(version)}"
        response = RequestHelper.post_v4_json(
            url=self.get_url(),
            endpoint=endpoint,
            content=json_data,
            token=self.get_token(),
            headers=headers
        )
        return IssueResponse(response) 