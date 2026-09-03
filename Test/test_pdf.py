import unittest
import os
import sys
import time
import uuid
from base64 import b64decode
from datetime import datetime, timedelta

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Pdf.Pdf import Pdf
from Utils.requestHelper import RequestHelper

class TestPdf(unittest.TestCase):
    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    uuidInvalid = "no-es-uuid"
    _uuidTimbrado = None

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
        #El UUID se toma de un CFDI timbrado en la propia cuenta, nunca se hardcodea, y
        #se prefiere uno que ya tenga PDF, que es el caso que ejercita la regeneración.
        if cls._uuidTimbrado is None:
            hasta = datetime.now()
            desde = hasta - timedelta(days=30)
            endpoint = (f"{cls.urlApi}/datawarehouse/v1/live/"
                        f"?startDate={desde.strftime('%Y-%m-%d')}&endDate={hasta.strftime('%Y-%m-%d')}")
            registros = RequestHelper.get_json_request(endpoint, cls.token).json()
            registros = registros.get("data", {}).get("records", [])
            if not registros:
                raise unittest.SkipTest("La cuenta de pruebas no tiene CFDI timbrados en los ultimos 30 dias")
            conPdf = [r for r in registros if r.get("urlPDF") or r.get("urlPdf")]
            cls._uuidTimbrado = (conPdf or registros)[0]["uuid"]
        return cls._uuidTimbrado

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
        with open('Test/resources/filePdf.pdf', 'wb') as file:
            file.write(bytes)

    def test_pdf_auth(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf(self.url,self.urlApi, None, self.user, self.password)
        response = pdf.generate_pdf(xml,logo, "cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_token(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf(self.url,self.urlApi,self.token)
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_error_token(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf(self.url,self.urlApi,"T2lYQ0t4.....")
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "error")
        
    def test_pdf_extras(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        pdf = Pdf(self.url,self.urlApi,self.token)
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        TestPdf.save_pdf(response.data['contentB64'])
        self.assertTrue(response.get_status() == "success")
        
    def test_pdf_all_one(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = None
        pdf = Pdf(self.url,self.urlApi,self.token)
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        self.assertIsNotNone(response.get_content_b64())
        self.assertTrue(response.get_content_size_bytes() > 0)
        self.assertIsNotNone(response.get_uuid())
        self.assertIsNotNone(response.get_folio())
        self.assertIsNotNone(response.get_stamp_date())
        self.assertIsNotNone(response.get_issued_date())
        self.assertIsNotNone(response.get_rfc_issuer())
        self.assertIsNotNone(response.get_rfc_receptor())
        self.assertIsNotNone(response.get_total())
        
    def test_pdf_all(self):
        xml = TestPdf.open_file("Test/resources/filePdf.xml")
        logo = None
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        pdf = Pdf(self.url,self.urlApi,self.token)
        response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
        self.assertTrue(response.get_status() == "success")
        self.assertIn("contentB64", response.response["data"])
        self.assertIn("uuid", response.response["data"])
        TestPdf.save_pdf(response.data['contentB64'])

    #UT Regeneración de PDF
    def test_regenerate_pdf_token(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf(self.stamped_uuid())
        self.assertTrue(response.get_status() == "success")
        self.assertTrue(200 == response.get_status_code())
        self.assertIn("correctamente", response.get_message())

    def test_regenerate_pdf_auth(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, None, self.user, self.password)
        response = pdf.regenerate_pdf(self.stamped_uuid())
        self.assertTrue(response.get_status() == "success")

    def test_regenerate_pdf_uuidObject(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf(uuid.UUID(self.stamped_uuid()))
        self.assertTrue(response.get_status() == "success")

    def test_regenerate_pdf_template_extras(self):
        extras = {
            'REFERENCIA': "Referencia de pruebas"
        }
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf(self.stamped_uuid(), None, "cfdi40", extras)
        self.assertTrue(response.get_status() == "success")

    #UT de Error
    def test_regenerate_pdf_notFound(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf(TestPdf.uuidNotFound)
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())
        self.assertIn("UUID", response.get_message())

    def test_regenerate_pdf_invalidFormat(self):
        TestPdf.esperar_limite()
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf(TestPdf.uuidInvalid)
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

    def test_regenerate_pdf_emptyString(self):
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, self.token)
        response = pdf.regenerate_pdf("")
        self.assertTrue(response.get_status() == "error")
        self.assertTrue(404 == response.get_status_code())

    def test_regenerate_pdf_invalidToken(self):
        pdf = Pdf(TestPdf.url, TestPdf.urlApi, "T2lYQ0t4.....")
        response = pdf.regenerate_pdf(self.stamped_uuid())
        self.assertTrue(response.get_status() == "error")
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPdf)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())