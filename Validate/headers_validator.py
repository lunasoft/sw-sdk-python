from typing import Optional, List
import re

class HeaderValidator:
    @staticmethod
    def validate_custom_id(custom_id: Optional[str]) -> Optional[str]:
        """
        Valida el encabezado custom_id
        - Debe ser una cadena de texto
        - Debe tener menos de 100 caracteres
        """
        if custom_id is None:
            return None
        if not isinstance(custom_id, str):
            raise ValueError("custom_id debe ser una cadena de texto")
        if len(custom_id) > 100:
            raise ValueError("custom_id debe tener menos de 100 caracteres")
        return custom_id

    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        """
        Valida el encabezado email
        - Debe ser una cadena de texto
        - Debe ser una lista de correos válidos separados por comas
        - Máximo 10 correos electrónicos permitidos
        """
        if email is None:
            return None
        if not isinstance(email, str):
            raise ValueError("email debe ser una cadena de texto")
        
        emails = [e.strip() for e in email.split(',')]
        if len(emails) > 10:
            raise ValueError("Máximo 10 correos electrónicos permitidos")
            
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for e in emails:
            if not re.match(email_pattern, e):
                raise ValueError(f"Formato de correo inválido: {e}")
        
        return email

    @staticmethod
    def validate_extra(extra: Optional[bool]) -> Optional[bool]:
        """
        Valida el encabezado extra
        - Debe ser un valor booleano
        """
        if extra is None:
            return None
        if not isinstance(extra, bool):
            raise ValueError("extra debe ser un valor booleano")
        return extra

    @staticmethod
    def get_headers(custom_id: Optional[str] = None, 
                    email: Optional[str] = None, 
                    extra: Optional[bool] = None) -> dict:
        """
        Valida y retorna un diccionario de encabezados
        
        Args:
            custom_id: Identificador personalizado opcional (texto < 100 caracteres)
            email: Lista opcional de correos separados por comas (máximo 10)
            extra: Bandera booleana opcional para generación de PDF
            
        Returns:
            dict: Diccionario de encabezados validados
        """
        headers = {}
        
        custom_id = HeaderValidator.validate_custom_id(custom_id)
        if custom_id is not None:
            headers['customid'] = custom_id
            
        email = HeaderValidator.validate_email(email)
        if email is not None:
            headers['email'] = email
            
        extra = HeaderValidator.validate_extra(extra)
        if extra:
            headers['pdf'] = 'true'
            
        return headers 