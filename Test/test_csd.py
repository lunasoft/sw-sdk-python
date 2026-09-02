import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Csd.Csd import Csd

class TestCsd(unittest.TestCase):
    expected = "success"
    url = "http://services.test.sw.com.mx"
    #Certificado de pruebas Test/resources/b64CSD.txt
    noCertificado = "30001000000500003416"
    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    def testUploadCsd_auth(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

    #UT Consulta de certificados
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

    #UT Consulta por tipo y certificado activo
    def testGetListCsdByType(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd_by_type("stamp")
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(isinstance(response.get_data(), list))
        for certificado in response.get_data():
            self.assertTrue("stamp" == certificado["certificate_type"])

    def testGetListCsdByType_withoutResults(self):
        #Un tipo sin certificados responde success con data vacío, no es un error.
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd_by_type("fiel")
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(isinstance(response.get_data(), list))

    def testGetActiveCsd(self):
        #El RFC y el tipo se toman de la propia cuenta, nunca se hardcodean.
        certificado = self.first_active_certificate()
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_active_csd(certificado["issuer_rfc"], certificado["certificate_type"])
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(isinstance(response.get_data(), dict))
        self.assertTrue(certificado["issuer_rfc"] == response.get_data()["issuer_rfc"])
        self.assertTrue(response.get_data()["is_active"])

    def testGetActiveCsd_rfcNotFound(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_active_csd("XAXX010101000", "stamp")
        self.assertTrue("error" == response.get_status())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacío")

    #UT de eliminación, destructiva: desactiva el CSD de pruebas recién cargado,
    #no el primero de la lista. Para rehabilitarlo basta con ejecutar testUploadCsd.
    @unittest.skipUnless(os.environ.get("SDKTEST_CSD_DELETE"), "Prueba destructiva, definir SDKTEST_CSD_DELETE para ejecutarla")
    def testDisableCsd(self):
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        upload = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"), "12345678a")
        self.assertTrue(self.expected == upload.get_status())
        certificate_number = TestCsd.noCertificado
        response = csd_obj.disable_csd(certificate_number)
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertTrue(certificate_number in str(response.get_data()))

    def first_active_certificate(self):
        """Regresa el primer certificado activo de la cuenta de pruebas.
        Omite la prueba si la cuenta no tiene ninguno activo."""
        csd_obj = Csd(TestCsd.url, os.environ["SDKTEST_TOKEN"])
        response = csd_obj.get_list_csd()
        self.assertTrue(self.expected == response.get_status())
        for certificado in response.get_data():
            if certificado["is_active"]:
                return certificado
        self.skipTest("La cuenta de pruebas no tiene certificados activos")

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCsd)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
