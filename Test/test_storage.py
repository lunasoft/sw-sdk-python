import unittest
import os
import sys
import requests

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Storage.Storage import Storage

class TestStorage(unittest.TestCase):
    expected = "success"
    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    #SDKTEST_UUID: UUID de un CFDI timbrado en la cuenta de pruebas, nunca de un cliente real.
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    uuidInvalid = "no-es-uuid"

    def test_get_by_uuid(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(os.environ["SDKTEST_UUID"])
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) > 0)
        self.assertIsNotNone(response.get_url_xml(), "El valor de urlXml esta vacio")

    def test_get_by_uuid_auth(self):
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = storage_obj.get_by_uuid(os.environ["SDKTEST_UUID"])
        self.assertTrue(self.expected == response.get_status())

    def test_get_by_uuid_notFound(self):
        #Un UUID inexistente responde success con records vacío, no es un error.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(TestStorage.uuidNotFound)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.get_records()) == 0)
        self.assertIsNone(response.get_url_xml())

    def test_get_by_uuid_invalidFormat(self):
        #PENDIENTE DE VERIFICAR CONTRA EL AMBIENTE: no se pudo ejecutar la consulta con un
        #UUID mal formado, así que se afirma únicamente el contrato común a las dos respuestas
        #posibles (400 con message, o 200 con records vacío). Al correrla se fija la aserción exacta.
        storage_obj = Storage(TestStorage.url, TestStorage.urlApi, os.environ["SDKTEST_TOKEN"])
        response = storage_obj.get_by_uuid(TestStorage.uuidInvalid)
        self.assertIsNotNone(response.get_status_code())
        self.assertIn(response.get_status(), ("success", "error"))
        if response.get_status() == "error":
            self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")
        else:
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
