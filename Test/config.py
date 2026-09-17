"""Configuración compartida de la suite de pruebas.

Todas las pruebas son de integración: pegan al ambiente de pruebas real de SW, de modo
que lo que se define aquí describe una cuenta concreta, no un ambiente cualquiera.

Los UUID están atados a esa cuenta. El datawarehouse está particionado por cuenta, así
que un comprobante timbrado en otra cuenta no resuelve con este token. Cuando una prueba
necesita un comprobante propio y reciente, lo busca en la cuenta durante la corrida en
lugar de fijarlo aquí. No agregar un UUID a mano a este archivo sin haber comprobado
antes que resuelve con las credenciales de abajo.
"""
import os

#Ambiente de pruebas de SW.
URL = "https://services.test.sw.com.mx"
URL_API = "https://api.test.sw.com.mx"

#El ambiente de pruebas expone el mismo servicio SOAP del SAT y resuelve los comprobantes
#timbrados en la cuenta, de modo que la consulta de estatus no necesita pegar a producción.
URL_SAT = "https://api.test.sw.com.mx/ConsultaCFDIService.svc"
SOAP_ACTION = "http://tempuri.org/IConsultaCFDIService/Consulta"

#Credenciales de la cuenta de pruebas.
USER = os.environ.get("SDKTEST_USER")
PASSWORD = os.environ.get("SDKTEST_PASSWORD")
TOKEN = os.environ.get("SDKTEST_TOKEN")

#Interruptores de las pruebas destructivas: dan de baja usuarios o certificados de la
#cuenta, así que sólo corren cuando se define la variable a propósito.
USER_LIFECYCLE = os.environ.get("SDKTEST_USER_LIFECYCLE")
CSD_DELETE = os.environ.get("SDKTEST_CSD_DELETE")

#Contraseña del CSD público de pruebas del SAT (Test/resources/b64CSD.txt).
PASSWORD_CSD = os.environ.get("SDKTEST_CSD_PASSWORD", "12345678a")

#RFC y número del certificado de pruebas Test/resources/b64CSD.txt.
RFC = "EKU9003173C9"
NO_CERTIFICADO = "30001000000500003416"

#Valores que los servicios rechazan, usados en las pruebas de error.
RFC_INVALID = "no-es-un-rfc"
ID_INVALID = "no-es-uuid"
ID_NOT_FOUND = "00000000-0000-0000-0000-000000000000"

#Datos con los que se dan de alta y se mueven de saldo las cuentas hijas.
TAX_ID = "XAXX010101000"
PHONE = "0000000000"
COMMENT = "Prueba unitaria Python"

#El servicio contesta 307 cuando el comprobante ya trae timbre, y 401 cuando la FechaExp
#del fixture rebasa las 72 horas. Los fixtures vienen sellados y el servicio valida el
#sello, de modo que la suite no puede refrescarles la fecha ni reemitirlos.
CODE_STAMPED = "307"
CODE_EXPIRED = "401"

#Comprobantes de la cuenta de pruebas sobre los que se ejercita cada servicio.
UUID_CANCELACION = "3dda215e-4c77-4923-94a1-627e0a04378c"
UUID_CANCELACION_RETENCION = "578052ce-710f-4d0b-9ffc-6ca73daf92a5"
UUID_ACEPTA_RECHAZA = "baf029f3-93ea-4267-a76c-1958d69bd4d8"
UUID_RELACIONES = "316dff4d-6a5a-40d5-8558-c8f45244aa90"

#El buscador del datawarehouse acepta rangos de hasta 30 días y responde vacío con rangos
#más largos, así que se recorre hacia atrás en tramos de 28.
TRAMOS_BUSQUEDA = 7
