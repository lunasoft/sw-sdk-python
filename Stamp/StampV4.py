from typing import Optional, Dict
from Utils.requestHelper import RequestHelper
from Utils.response_version import ResponseVersion
from Stamp.StampResponse import StampResponse
from Utils.Services import Services

class StampV4(Services):
    """Clase para el servicio Stamp V4 que soporta versiones de respuesta"""
    
    def __init__(self, url: str, token: str = None, user: str = None, password: str = None):
        """
        Inicializa el servicio Stamp V4
        
        Args:
            url: URL base del servicio
            token: Token de autenticación (opcional)
            user: Usuario para autenticación (opcional)
            password: Contraseña para autenticación (opcional)
        """
        super(StampV4, self).__init__(url, token, user, password)
        
    def stamp(self, xml: str, headers: Optional[Dict] = None, version: ResponseVersion = ResponseVersion.V1) -> StampResponse:
        """
        Timbra un XML usando el servicio V4
        
        Args:
            xml: String del XML a timbrar
            headers: Headers opcionales (customid, email, etc)
            version: Versión de respuesta (default: V1)
            
        Returns:
            StampResponse: Respuesta del servicio
        """
        endpoint = f"/v4/cfdi33/stamp/{str(version)}"
        response = RequestHelper.post_v4(
            url=self.get_url(),
            endpoint=endpoint,
            content=xml,
            token=self.get_token(),
            headers=headers
        )
        return StampResponse(response) 