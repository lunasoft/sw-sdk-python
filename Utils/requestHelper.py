import requests
import random
import string
from typing import Union, Dict, Optional
from .response_version import ResponseVersion
from datetime import datetime
import json

class RequestHelper:
    @staticmethod
    def _get_session():
        """Obtiene una sesión HTTP configurada"""
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter()
        session.mount("https://", adapter)
        return session
    
    @staticmethod
    def post_json_request_Without_Headers(endpoint, payload, headers=None):
        """Realiza una petición POST JSON sin headers predefinidos"""
        session = RequestHelper._get_session()
        response = session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def post_json_request(endpoint, token, payload=None):
        """Realiza una petición POST JSON con token de autenticación"""
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json",'Cache-Control': "no-cache"}
        response = session.post(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def post_jsontoxml_request(endpoint, token, payload=None):
        """Realiza una petición POST para convertir JSON a XML"""
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/jsontoxml; charset=utf-8",'Cache-Control': "no-cache"}
        response = session.post(endpoint, data=payload.encode('utf-8'), headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def get_json_request(endpoint, token, payload=None):
        """Realiza una petición GET JSON"""
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json",'Cache-Control': "no-cache"}
        response = session.get(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def delete_json_request(endpoint, token, payload=None):
        """Realiza una petición DELETE JSON"""
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json",'Cache-Control': "no-cache"}
        response = session.delete(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
    
    @staticmethod
    def put_json_request(endpoint, token, payload=None):
        """Realiza una petición PUT JSON"""
        session = RequestHelper._get_session()
        headers = {'Authorization': f"bearer {token}",'Content-Type': "application/json",'Cache-Control': "no-cache"}
        response = session.put(endpoint, json=payload, headers=headers, verify=True, timeout=300)
        return response
        
    @staticmethod
    def post_multipart_request(endpoint, token, xml_data):
        """Realiza una petición POST multipart/form-data"""
        session = RequestHelper._get_session()
        boundary = "".join(random.choices(string.ascii_letters + string.digits, k=30))
        payload = (
            f"--{boundary}\r\n"
            "Content-Type: text/xml\r\n"
            "Content-Transfer-Encoding: binary\r\n"
            'Content-Disposition: form-data; name="xml"; filename="xml"\r\n\r\n'
            f"{str(xml_data)}\r\n"
            f"--{boundary}--"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": f'multipart/form-data; boundary={boundary}'
        }
        response = session.post(endpoint, data=payload.encode('utf-8'), headers=headers, verify=True, timeout=300)
        return response

    @staticmethod
    def authenticate(url: str, user: str, password: str) -> dict:
        """
        Realiza la autenticación usando usuario y contraseña
        
        Args:
            url: URL base del servicio
            user: Usuario para autenticación
            password: Contraseña para autenticación
            
        Returns:
            dict: Respuesta con el token
        """
        auth_url = f"{url}/security/authenticate"
        payload = {
            "user": user,
            "password": "****"  # Ocultamos la contraseña en los logs
        }
        real_payload = {
            "user": user,
            "password": password
        }
        response = requests.post(auth_url, json=real_payload)
        return response.json()

    @staticmethod
    def build_endpoint(base_url: str, endpoint: str) -> str:
        """
        Construye el endpoint completo
        
        Args:
            base_url: URL base del servicio
            endpoint: Endpoint base
            
        Returns:
            str: Endpoint completo
        """
        base_url = base_url.rstrip('/')
        endpoint = endpoint.strip('/')
        return f"{base_url}/{endpoint}"

    @staticmethod
    def _create_multipart_body(content: Union[str, dict], boundary: str) -> bytes:
        """
        Crea el cuerpo multipart/form-data para la petición
        
        Args:
            content: Contenido a enviar (XML string o JSON dict)
            boundary: Boundary para separar las partes del multipart
            
        Returns:
            bytes: Cuerpo de la petición en bytes
        """
        # Si es un diccionario, convertirlo a string JSON
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
            
        # Crear el cuerpo multipart
        body = (
            f"--{boundary}\r\n"
            "Content-Type: text/xml\r\n"
            "Content-Transfer-Encoding: binary\r\n"
            'Content-Disposition: form-data; name="xml"; filename="xml"\r\n\r\n'
            f"{str(content)}\r\n"
            f"--{boundary}--"
        )
        
        return body.encode('utf-8')

    @staticmethod
    def post_v4_json(url: str, endpoint: str, content: Union[str, dict], token: str = None,
                headers: Dict = None, user: str = None, password: str = None) -> requests.Response:
        """
        Realiza una petición POST para servicios V4 con contenido JSON
        
        Args:
            url: URL base del servicio
            endpoint: Endpoint del servicio
            content: Contenido JSON a enviar (como string o dict)
            token: Token de autenticación (opcional)
            headers: Headers adicionales (opcional)
            user: Usuario para autenticación (opcional)
            password: Contraseña para autenticación (opcional)
            
        Returns:
            requests.Response: Objeto response completo
        """
        # Si no hay token pero hay credenciales, obtener token
        if not token and user and password:
            auth_response = RequestHelper.authenticate(url, user, password)
            token = auth_response.get_token()
        
        # Preparar headers
        request_headers = {
            'Authorization': f'Bearer {token}' if token else None,
            'Content-Type': 'application/jsontoxml; charset=utf-8'
        }
        
        # Agregar headers adicionales
        if headers:
            request_headers.update(headers)
            
        # Construir URL completa
        complete_url = f"{url}{endpoint}"
        
        # Si el contenido es un diccionario, convertirlo a string
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        
        # Realizar petición POST
        response = requests.post(complete_url, data=content.encode('utf-8'), headers=request_headers)
        
        # No lanzar excepción para errores 400, ya que pueden ser errores de negocio como el 307
        if response.status_code >= 500:
            response.raise_for_status()
            
        return response

    @staticmethod
    def post_v4(url: str, endpoint: str, content: Union[str, dict], token: str = None,
                headers: Dict = None, user: str = None, password: str = None) -> requests.Response:
        """
        Realiza una petición POST para servicios V4 con contenido XML
        
        Args:
            url: URL base del servicio
            endpoint: Endpoint del servicio
            content: Contenido XML a enviar
            token: Token de autenticación (opcional)
            headers: Headers adicionales (opcional)
            user: Usuario para autenticación (opcional)
            password: Contraseña para autenticación (opcional)
            
        Returns:
            requests.Response: Objeto response completo
        """
        # Si no hay token pero hay credenciales, obtener token
        if not token and user and password:
            auth_response = RequestHelper.authenticate(url, user, password)
            token = auth_response.get_token()
        
        # Preparar headers
        request_headers = {
            'Authorization': f'Bearer {token}' if token else None,
        }
        
        # Agregar headers adicionales
        if headers:
            request_headers.update(headers)
            
        # Construir URL completa
        complete_url = f"{url}{endpoint}"
        
        # Preparar contenido como multipart/form-data
        boundary = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        request_headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        
        # Crear el cuerpo multipart
        body = RequestHelper._create_multipart_body(content, boundary)
        
        # Realizar petición POST
        response = requests.post(complete_url, data=body, headers=request_headers)
        
        # No lanzar excepción para errores 400, ya que pueden ser errores de negocio como el 307
        if response.status_code >= 500:
            response.raise_for_status()
            
        return response