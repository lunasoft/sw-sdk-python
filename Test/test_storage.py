import unittest
import os
import sys
import uuid
import requests

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Storage.Storage import Storage

class TestStorage(unittest.TestCase):
    expected = "success"
    url = "http://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    #SDKTEST_UUID: UUID de un CFDI timbrado en la cuenta de pruebas, nunca de un cliente real.
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    uuidInvalid = "no-es-uuid"

    #UT Recuperación de XML por UUID
    def test_get_by_uuid(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(os.environ["SDKTEST_UUID"])
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) > 0)
        self.assertTrue(os.environ["SDKTEST_UUID"] == response.get_first_record()["uuid"])
        self.assertIsNotNone(response.get_url_xml(), "El valor de urlXml esta vacio")

    def test_get_by_uuid_uuidObject(self):
        #El UUID también se acepta como uuid.UUID, no sólo como cadena.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(uuid.UUID(os.environ["SDKTEST_UUID"]))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(os.environ["SDKTEST_UUID"] == response.get_first_record()["uuid"])

    def test_get_by_uuid_auth(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = storage_obj.get_by_uuid(os.environ["SDKTEST_UUID"])
        self.assertTrue(self.expected == response.get_status())

    #UT Consultas sin coincidencias
    def test_get_by_uuid_notFound(self):
        #Un UUID inexistente responde success con records vacío, no es un error.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(TestStorage.uuidNotFound)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) == 0)
        self.assertIsNone(response.get_url_xml())

    def test_get_by_uuid_invalidFormat(self):
        #Un UUID mal formado responde igual que uno inexistente: 200 success con records
        #vacío y sin message. El servicio no valida el formato.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(TestStorage.uuidInvalid)
        self.assertTrue(200 == response.get_status_code())
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) == 0)

    #UT de Error
    def test_get_by_uuid_emptyString(self):
        #Una cadena vacía deja la ruta en /datawarehouse/v1/live/, que es el buscador por
        #fechas: responde 400 pidiendo la fecha de inicio. No regresa un recurso distinto
        #al pedido, así que el valor se envía tal cual y responde el servicio.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
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
        storage_obj = Storage(TestStorage.url, "", os.environ["SDKTEST_TOKEN"])
        with self.assertRaises(requests.exceptions.RequestException):
            storage_obj.get_by_uuid(TestStorage.uuidNotFound)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStorage)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
