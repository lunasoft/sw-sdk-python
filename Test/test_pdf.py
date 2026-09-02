import unittest
import os
import sys
import time
import uuid
from base64 import b64decode

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Pdf.Pdf import Pdf

class TestPdf(unittest.TestCase):
    url = "http://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    uuidTest = "3001449c-ef91-4bd5-a698-687bdea46414"
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    uuidInvalid = "no-es-uuid"

    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    @staticmethod
    def esperar_limite():
        #La regeneración responde 429 cuando se consumen varias peticiones seguidas.
        time.sleep(3)

    @staticmethod
    def save_pdf(contentB64):
        bytes = b64decode(contentB64, validate=True)
        f = open('Test/resources/filePdf.pdf', 'wb')
        f.write(bytes)
        f.close()

    def test_pdf_auth(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        response = pdf.generate_pdf(xml,logo, "cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_token(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx",os.environ['SDKTEST_TOKEN'])
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_error_token(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx","T2lYQ0t4.....")
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "error")
        
    def test_pdf_extras(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx",os.environ['SDKTEST_TOKEN'])
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        TestPdf.save_pdf(response.data['contentB64'])
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_all_one(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx",os.environ['SDKTEST_TOKEN'])
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        print("Datos")
        #print("Content B64: ", response.get_content_b64())
        print("Content Size Bytes: ", response.get_content_size_bytes())
        print("UUID: ", response.get_uuid())
        print("Serie: ", response.get_serie())
        print("Folio: ", response.get_folio())
        print("Stamp Date: ", response.get_stamp_date())
        print("Issuer Date: ", response.get_issued_date())
        print("RFC Issuer: ", response.get_rfc_issuer())
        print("RFC Receptor: ", response.get_rfc_receptor())
        print("Total: ", response.get_total())
        
    def test_pdf_all(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx",os.environ['SDKTEST_TOKEN'])
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        print("Datos")
        for Key,Value in response.response["data"].items():
            print (Key,"=",Value)
        TestPdf.save_pdf(response.data['contentB64'])

    #UT Regeneración de PDF
    def test_regenerate_pdf_token(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf(TestPdf.uuidTest)
        self.assertTrue(response.get_status() == "success")
        self.assertTrue(200 == response.get_status_code())
        self.assertIn("correctamente", response.get_message())

    def test_regenerate_pdf_auth(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        response = pdf.regenerate_pdf(TestPdf.uuidTest)
        self.assertTrue(response.get_status() == "success")

    def test_regenerate_pdf_uuidObject(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf(uuid.UUID(TestPdf.uuidTest))
        self.assertTrue(response.get_status() == "success")

    def test_regenerate_pdf_template_extras(self):
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf(TestPdf.uuidTest, None, "cfdi40", extras)
        self.assertTrue(response.get_status() == "success")

    #UT de Error
    def test_regenerate_pdf_notFound(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf(TestPdf.uuidNotFound)
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())
        self.assertIn("UUID", response.get_message())

    def test_regenerate_pdf_invalidFormat(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf(TestPdf.uuidInvalid)
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

    def test_regenerate_pdf_emptyString(self):
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, os.environ['SDKTEST_TOKEN'])
        response = pdf.regenerate_pdf("")
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())

    def test_regenerate_pdf_invalidToken(self):
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, "T2lYQ0t4.....")
        response = pdf.regenerate_pdf(TestPdf.uuidTest)
        self.assertTrue(response.get_status() == "error")
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPdf)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())