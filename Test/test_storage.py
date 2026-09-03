import unittest
import os
import sys
import uuid
from datetime import datetime, timedelta
import requests

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Storage.Storage import Storage
from Utils.requestHelper import RequestHelper

class TestStorage(unittest.TestCase):
    expected = "success"
    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    uuidInvalid = "no-es-uuid"
    _uuidTimbrado = None

    #Las credenciales de la cuenta de pruebas nunca van en el codigo.
    user = os.environ.get("SDKTEST_USER")
    password = os.environ.get("SDKTEST_PASSWORD")
    token = os.environ.get("SDKTEST_TOKEN")

    @classmethod
    def setUpClass(cls):
        for nombre, valor in (("SDKTEST_USER", cls.user),
                              ("SDKTEST_PASSWORD", cls.password),
                              ("SDKTEST_TOKEN", cls.token)):
            if not valor:
                raise ValueError(f"Falta la variable de entorno {nombre}")

    @classmethod
    def stamped_uuid(cls):
        #El UUID se toma de un CFDI timbrado en la propia cuenta, nunca se hardcodea:
        #se consultan los timbrados de los ultimos 30 dias por rango de fechas.
        if cls._uuidTimbrado is None:
            hasta = datetime.now()
            desde = hasta - timedelta(days=30)
            endpoint = (f"{cls.urlApi}/datawarehouse/v1/live/"
                        f"?startDate={desde.strftime('%Y-%m-%d')}&endDate={hasta.strftime('%Y-%m-%d')}")
            registros = RequestHelper.get_json_request(endpoint, cls.token).json()
            registros = registros.get("data", {}).get("records", [])
            if not registros:
                raise unittest.SkipTest("La cuenta de pruebas no tiene CFDI timbrados en los ultimos 30 dias")
            cls._uuidTimbrado = registros[0]["uuid"]
        return cls._uuidTimbrado

    #UT Recuperación de XML por UUID
    def test_get_by_uuid(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, self.token)
        uuidTimbrado = self.stamped_uuid()
        response = storage_obj.get_by_uuid(uuidTimbrado)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) > 0)
        self.assertTrue(uuidTimbrado == response.get_first_record()["uuid"])
        self.assertIsNotNone(response.get_url_xml(), "El valor de urlXml esta vacio")

    def test_get_by_uuid_uuidObject(self):
        #El UUID también se acepta como uuid.UUID, no sólo como cadena.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, self.token)
        uuidTimbrado = self.stamped_uuid()
        response = storage_obj.get_by_uuid(uuid.UUID(uuidTimbrado))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(uuidTimbrado == response.get_first_record()["uuid"])

    def test_get_by_uuid_auth(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, None, self.user, self.password)
        response = storage_obj.get_by_uuid(self.stamped_uuid())
        self.assertTrue(self.expected == response.get_status())

    #UT Consultas sin coincidencias
    def test_get_by_uuid_notFound(self):
        #Un UUID inexistente responde success con records vacío, no es un error.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, self.token)
        response = storage_obj.get_by_uuid(TestStorage.uuidNotFound)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) == 0)
        self.assertIsNone(response.get_url_xml())

    def test_get_by_uuid_invalidFormat(self):
        #Un UUID mal formado responde igual que uno inexistente: 200 success con records
        #vacío y sin message. El servicio no valida el formato.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, self.token)
        response = storage_obj.get_by_uuid(TestStorage.uuidInvalid)
        self.assertTrue(200 == response.get_status_code())
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) == 0)

    #UT de Error
    def test_get_by_uuid_emptyString(self):
        #Una cadena vacía deja la ruta en /datawarehouse/v1/live/, que es el buscador por
        #fechas: responde 400 pidiendo la fecha de inicio. No regresa un recurso distinto
        #al pedido, así que el valor se envía tal cual y responde el servicio.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, self.token)
        response = storage_obj.get_by_uuid("")
        self.assertTrue("error" == response.get_status())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")
        self.assertTrue(len(response.get_records()) == 0)

    def test_get_by_uuid_invalidToken(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, "T2lYQ0t4.....")
        response = storage_obj.get_by_uuid(TestStorage.uuidNotFound)
        self.assertTrue("error" == response.get_status())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

    def test_get_by_uuid_withoutUrlApi(self):
        #Con urlApi vacía la librería avisa por consola igual que Pdf y AccountUser, y la
        #petición no se puede armar. Se documenta el comportamiento actual del repositorio.
        storage_obj = Storage(TestStorage.url, "", self.token)
        with self.assertRaises(requests.exceptions.RequestException):
            storage_obj.get_by_uuid(TestStorage.uuidNotFound)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStorage)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
