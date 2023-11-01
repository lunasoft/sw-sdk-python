import unittest
import os 
import sys
from base64 import b64decode

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Pdf.Pdf import Pdf

class TestPdf(unittest.TestCase):
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile,"r", encoding='latin_1', errors='ignore').read()
        return out
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
        print("Content B64: ", response.get_content_b64())
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

suite = unittest.TestLoader().loadTestsFromTestCase(TestPdf)
unittest.TextTestRunner(verbosity=2).run(suite)