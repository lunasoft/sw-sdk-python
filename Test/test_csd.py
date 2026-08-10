import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Csd.Csd import Csd
from Csd.CsdResponse import CsdResponse

class TestCsd(unittest.TestCase):
    expected = "success"
    url = "http://services.test.sw.com.mx"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testUploadCsd_auth(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

    #Consulta de certificados
    def testGetListCsd(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd()
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(isinstance(response.get_data(), list))

    def testGetListCsd_auth(self):
        csd_obj = Csd(TestCsd.url, None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = csd_obj.get_list_csd()
        self.assertTrue(self.expected == response.get_status())

    def testGetCsd(self):
        #El número de certificado se toma de la propia cuenta, nunca se hardcodea.
        certificate_number = self.first_certificate()["certificate_number"]
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_csd(certificate_number)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(certificate_number == response.get_data()["certificate_number"])

    def testGetCsd_notFound(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_csd("00000000000000000000")
        self.assertTrue("error" == response.get_status())
        self.assertIsNotNone(response.get_messageDetail(), "El valor de messageDetail esta vacio")

    def testGetListCsdByRfc(self):
        rfc = self.first_certificate()["issuer_rfc"]
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd_by_rfc(rfc)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(isinstance(response.get_data(), list))

    def testGetListCsd_invalidToken(self):
        csd_obj = Csd(TestCsd.url, "T2lYQ0t4.....")
        response = csd_obj.get_list_csd()
        self.assertTrue("error" == response.get_status())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

    #Validación de parámetros: falla antes de ejecutar la petición
    def testGetCsd_emptyCertificateNumber(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        with self.assertRaises(ValueError) as context:
            csd_obj.get_csd("")
        self.assertTrue("Debe especificar el número de certificado" == str(context.exception))

    def testGetCsd_noneCertificateNumber(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        with self.assertRaises(ValueError):
            csd_obj.get_csd(None)

    def testDisableCsd_emptyCertificateNumber(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        with self.assertRaises(ValueError):
            csd_obj.disable_csd("   ")

    def testGetListCsdByRfc_emptyRfc(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        with self.assertRaises(ValueError) as context:
            csd_obj.get_list_csd_by_rfc(None)
        self.assertTrue("Debe especificar el RFC" == str(context.exception))

    #Eliminación de certificado: destructiva sobre la cuenta de pruebas.
    #Sube el CSD de pruebas, ubica su número y desactiva ese mismo certificado,
    #nunca el primero de la lista, que puede pertenecer a otro RFC.
    #Para volver a habilitarlo basta con ejecutar testUploadCsd.
    @unittest.skipUnless(os.environ.get("SDKTEST_CSD_DELETE"), "Prueba destructiva, definir SDKTEST_CSD_DELETE para ejecutarla")
    def testDisableCsd(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        b64_cert = TestCsd.open_file("Test/resources/b64CSD.txt")
        upload = csd_obj.upload_csd("stamp", b64_cert, TestCsd.open_file("Test/resources/b64Key.txt"), "12345678a")
        self.assertTrue(self.expected == upload.get_status())
        certificate_number = self.certificate_number_of(b64_cert)
        response = csd_obj.disable_csd(certificate_number)
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertTrue(certificate_number in str(response.get_data()))

    def certificate_number_of(self, b64_cert):
        """Ubica en la cuenta el certificado cuyo Base64 coincide con el recibido.
        upload_csd sólo regresa un texto de confirmación, sin el número de certificado."""
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd()
        self.assertTrue(self.expected == response.get_status())
        for certificado in response.get_data():
            if certificado["csd_certificate"].strip() == b64_cert.strip():
                return certificado["certificate_number"]
        self.fail("No se encontró en la cuenta el certificado de pruebas recién cargado")

    def first_certificate(self):
        """Regresa el primer certificado listado en la cuenta de pruebas.
        Omite la prueba si la cuenta no tiene certificados cargados."""
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd()
        self.assertTrue(self.expected == response.get_status())
        data = response.get_data()
        if not data:
            self.skipTest("La cuenta de pruebas no tiene certificados cargados")
        return data[0]

class FakeResponse:
    """Respuesta simulada de requests, para probar el parseo de CsdResponse sin red."""
    def __init__(self, status_code, text, reason = "Bad Request"):
        self.status_code = status_code
        self.text = text
        self.reason = reason
        self.request = None

class TestCsdResponse(unittest.TestCase):
    """Pruebas del parseo de CsdResponse. No requieren credenciales ni red."""

    def testParse_dataList(self):
        body = '{"data":[{"certificate_number":"30001000000400002434","issuer_rfc":"EKU9003173C9"}],"status":"success"}'
        response = CsdResponse(FakeResponse(200, body))
        self.assertTrue("success" == response.get_status())
        self.assertTrue(isinstance(response.get_data(), list))
        self.assertTrue("30001000000400002434" == response.get_data()[0]["certificate_number"])

    def testParse_dataDict(self):
        body = '{"data":{"certificate_number":"30001000000400002434","is_active":true},"status":"success"}'
        response = CsdResponse(FakeResponse(200, body))
        self.assertTrue("success" == response.get_status())
        self.assertTrue(isinstance(response.get_data(), dict))
        self.assertTrue("30001000000400002434" == response.get_data()["certificate_number"])

    def testParse_dataString(self):
        body = '{"data":"Certificado 30001000000400002434 desactivado.","status":"success"}'
        response = CsdResponse(FakeResponse(200, body))
        self.assertTrue("success" == response.get_status())
        self.assertTrue("Certificado 30001000000400002434 desactivado." == response.get_data())

    def testParse_error(self):
        #Regresión: antes de esta versión status quedaba en None en la rama de error.
        body = '{"message":"Certificado no encontrado","messageDetail":"Detalle del error","data":null,"status":"error"}'
        response = CsdResponse(FakeResponse(400, body))
        self.assertTrue("error" == response.get_status())
        self.assertTrue("Certificado no encontrado" == response.get_message())
        self.assertTrue("Detalle del error" == response.get_messageDetail())

    def testParse_emptyBody(self):
        response = CsdResponse(FakeResponse(500, "", "Internal Server Error"))
        self.assertTrue("error" == response.get_status())
        self.assertTrue("Internal Server Error" == response.get_message())

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite([loader.loadTestsFromTestCase(TestCsd),
                                loader.loadTestsFromTestCase(TestCsdResponse)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
