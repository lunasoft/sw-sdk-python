"""Clase base de la suite de pruebas.

Todas las pruebas son de integración contra el ambiente real y necesitan lo mismo: las
URL, las credenciales de la cuenta, una forma de leer los fixtures y, en varios casos,
un comprobante o una cuenta hija de la propia cuenta de pruebas. Heredar de SdkTestCase
evita repetirlo en cada archivo.

La consulta de estatus es la excepción: va directo al SAT, no usa credenciales, y por eso
sigue extendiendo unittest.TestCase.
"""
import unittest
from datetime import datetime, timedelta

from Test import config
from AccountUser.AccountUser import AccountUser
from Utils.requestHelper import RequestHelper


class SdkTestCase(unittest.TestCase):
    expected = "success"
    expectedError = "error"

    url = config.URL
    url_api = config.URL_API
    user = config.USER
    password = config.PASSWORD
    token = config.TOKEN

    #La autenticación es la única que no usa token, de modo que cada clase declara lo que
    #realmente necesita para correr.
    requeridas = ("SDKTEST_USER", "SDKTEST_PASSWORD", "SDKTEST_TOKEN")

    #El PDF sólo se puede regenerar sobre un comprobante que ya tuvo uno: regenerar uno
    #que nunca lo tuvo responde 404.
    exigePdf = False

    #Lo que se encuentra en la cuenta se guarda para no repetir la consulta en cada prueba.
    _uuidTimbrado = None
    _firstUser = None

    @classmethod
    def setUpClass(cls):
        entorno = {"SDKTEST_USER": cls.user,
                   "SDKTEST_PASSWORD": cls.password,
                   "SDKTEST_TOKEN": cls.token}
        for nombre in cls.requeridas:
            if not entorno[nombre]:
                raise ValueError(f"Falta la variable de entorno {nombre}")

    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out

    @classmethod
    def stamped_uuid(cls):
        #El UUID se toma de un CFDI timbrado en la propia cuenta, nunca se hardcodea: el
        #datawarehouse está particionado por cuenta, de modo que un UUID fijo sólo resuelve
        #con el token de la cuenta que timbró el comprobante.
        if cls._uuidTimbrado is None:
            #El buscador por fechas acepta rangos de hasta 30 días y responde vacío con
            #rangos más largos, así que se recorre hacia atrás por tramos.
            for tramo in range(config.TRAMOS_BUSQUEDA):
                hasta = datetime.now() - timedelta(days=28 * tramo)
                desde = hasta - timedelta(days=28)
                endpoint = (f"{cls.url_api}/datawarehouse/v1/live/"
                            f"?startDate={desde.strftime('%Y-%m-%d')}&endDate={hasta.strftime('%Y-%m-%d')}")
                registros = RequestHelper.get_json_request(endpoint, cls.token).json()
                registros = registros.get("data", {}).get("records", [])
                if cls.exigePdf:
                    registros = [r for r in registros if r.get("urlPDF") or r.get("urlPdf")]
                if registros:
                    cls._uuidTimbrado = registros[0]["uuid"]
                    break
            if cls._uuidTimbrado is None:
                mensaje = "La cuenta de pruebas no tiene CFDI timbrados"
                if cls.exigePdf:
                    mensaje += " con PDF"
                raise unittest.SkipTest(mensaje)
        return cls._uuidTimbrado

    @classmethod
    def first_user(cls):
        #Los datos de consulta se toman de la propia cuenta, nunca se hardcodean.
        if cls._firstUser is None:
            accountUser = AccountUser(cls.url, cls.url_api, cls.token)
            response = accountUser.get_users()
            if response.get_status() != cls.expected or not response.data.items:
                raise unittest.SkipTest("La cuenta de pruebas no tiene cuentas hijas")
            cls._firstUser = response.data.items[0]
        return cls._firstUser
