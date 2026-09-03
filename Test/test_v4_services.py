import unittest
import os
import sys
import json
from base64 import b64encode
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
import random
import string
import time

PROJECT_ROOT = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, PROJECT_ROOT)

from Issue.IssueV4 import IssueV4
from Stamp.StampV4 import StampV4
from Storage.Storage import Storage
from Utils.response_version import ResponseVersion

class TestV4Basic(unittest.TestCase):

    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
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

    @staticmethod
    def generate_custom_id(prefix):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=2))
        timestamp = datetime.now().strftime("%H%M")
        return f"{prefix}-{letters}{numbers}-{timestamp}"

    @staticmethod
    def update_date_xml(path_xml):
        ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}
        tree = ET.parse(path_xml)
        root = tree.getroot()

        new_date = datetime.now() - timedelta(hours=1)
        if "Fecha" not in root.attrib:
            raise ValueError("No se encontró el atributo 'Fecha' en el XML")
        root.set("Fecha", new_date.strftime("%Y-%m-%dT%H:%M:%S"))
        ET.register_namespace("cfdi", ns["cfdi"])
        xml_buffer = BytesIO()
        tree.write(xml_buffer, encoding="utf-8", xml_declaration=True)
        return xml_buffer.getvalue().decode("utf-8")

    @staticmethod
    def update_date_json(path_json):
        with open(path_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        new_date = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        if "Fecha" not in data:
            raise ValueError("No se encontró la clave 'Fecha' en el JSON")
        data["Fecha"] = new_date
        return json.dumps(data, indent=2, ensure_ascii=False)

    def wait_url_pdf(self, uuid):
        #El PDF del comprobante tarda en quedar disponible en el ADT: el registro aparece
        #alrededor de los 70 segundos y la urlPDF hasta los 110, con variacion segun la
        #carga del ambiente. Se consulta cada 5 segundos hasta 5 minutos y se regresa en
        #cuanto esta lista, de modo que la espera real sigue siendo la del servicio.
        storage = Storage(self.url, self.urlApi, self.token)
        for _ in range(60):
            time.sleep(5)
            url_pdf = storage.get_by_uuid(uuid).get_url_pdf()
            if url_pdf:
                return url_pdf
        return None

    #UT Emisión de Timbrado XML
    def test_issue_xml_auth_named_params(self):
        issue = IssueV4(self.url, None, self.user, self.password)
        xml_content = self.update_date_xml("Test/resources/xml40.xml")

        response = issue.issue_xml(xml_content,
                                   custom_id=self.generate_custom_id("ISS"),
                                   email=["test1@test.com", "test2@test.com"],
                                   pdf=True,
                                   version=ResponseVersion.V4)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data.get("cfdi"))
        self.assertIsNotNone(response.data.get("uuid"))
        self.assertIsNotNone(self.wait_url_pdf(response.data.get("uuid")),
                             "El comprobante se timbró sin generar el PDF en el ADT")

    def test_issue_xml_token_minimal_headers(self):
        issue = IssueV4(self.url, self.token)
        xml_content = self.update_date_xml("Test/resources/xml40.xml")

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V3)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data.get("cfdi"))

    def test_issue_xml_headers_over_named_params(self):
        issue = IssueV4(self.url, self.token)
        xml_content = self.update_date_xml("Test/resources/xml40.xml")

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response1 = issue.issue_xml(xml_content, headers=headers,
                                    custom_id=self.generate_custom_id("OTR"),
                                    version=ResponseVersion.V4)

        self.assertEqual("success", response1.get_status())
        self.assertEqual(200, response1.status_code)

        #El customid que llegó al servicio es el del diccionario: al repetirlo responde con el timbre previo.
        response2 = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response2.get_status())
        self.assertIn("307", response2.get_message())

    def test_issue_xml_b64(self):
        issue = IssueV4(self.url, self.token)
        xml_content = self.update_date_xml("Test/resources/xml40.xml")
        xml_b64 = b64encode(xml_content.encode("utf-8")).decode()

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response = issue.issue_xml(xml_b64, headers=headers, version=ResponseVersion.V4, b64=True)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data.get("uuid"))

    #UT Timbrado XML
    def test_stamp_token_all_headers(self):
        stamp = StampV4(self.url, self.token)
        xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()

        headers = {
            "customid": self.generate_custom_id("STP"),
            "email": "stamp1@test.com,stamp2@test.com",
            "extra": "pdf"
        }

        response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V2)

        if response.get_status() == "error":
            self.assertIn("307", response.get_message())
        else:
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data.get("tfd"))

    def test_stamp_auth_email_only(self):
        stamp = StampV4(self.url, None, self.user, self.password)
        xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()

        headers = {
            "email": "stamp1@test.com"
        }

        response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)

        if response.get_status() == "error":
            self.assertIn("307", response.get_message())
        else:
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)

    def test_stamp_b64(self):
        stamp = StampV4(self.url, self.token)
        xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()
        xml_b64 = b64encode(xml_content.encode("utf-8")).decode()

        headers = {
            "customid": self.generate_custom_id("STP")
        }

        response = stamp.stamp(xml_b64, headers=headers, version=ResponseVersion.V2, b64=True)

        if response.get_status() == "error":
            self.assertIn("307", response.get_message())
        else:
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)

    #UT Emisión de Timbrado JSON
    def test_issue_json_auth_all_headers(self):
        issue = IssueV4(self.url, None, self.user, self.password)
        json_content = self.update_date_json("Test/resources/cfdi.json")

        headers = {
            "customid": self.generate_custom_id("ISJ"),
            "email": "test1@test.com,test2@test.com"
        }

        response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data.get("cfdi"))
        self.assertIsNotNone(response.data.get("uuid"))

    def test_issue_json_token_minimal_headers(self):
        issue = IssueV4(self.url, self.token)
        time.sleep(5)
        json_content = self.update_date_json("Test/resources/cfdi.json")

        headers = {
            "customid": self.generate_custom_id("ISJ")
        }

        response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V3)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data.get("cfdi"))

    def test_issue_json_with_pdf(self):
        issue = IssueV4(self.url, self.token)
        time.sleep(5)
        json_content = self.update_date_json("Test/resources/cfdi.json")

        headers = {
            "customid": self.generate_custom_id("ISJ"),
            "email": "test1@test.com",
            "extra": "pdf"
        }

        response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("success", response.get_status())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data.get("uuid"))
        self.assertIsNotNone(self.wait_url_pdf(response.data.get("uuid")),
                             "El comprobante se timbró sin generar el PDF en el ADT")

    #UT de Error
    def test_issue_xml_invalid_credentials(self):
        issue = IssueV4(self.url, None, "usuario_invalido", "pass_invalido")
        xml_content = self.update_date_xml("Test/resources/xml40.xml")

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response.get_status())
        self.assertNotEqual(200, response.status_code)
        self.assertIsNone(response.data)
        self.assertIn("AU4101", response.get_message())

    def test_issue_xml_invalid_xml(self):
        issue = IssueV4(self.url, self.token)

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response = issue.issue_xml("<xml>mal formado</xml>", headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response.get_status())
        self.assertNotEqual(200, response.status_code)
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

    def test_stamp_invalid_token(self):
        stamp = StampV4(self.url, "token_invalido")
        xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()

        headers = {
            "customid": self.generate_custom_id("STP")
        }

        response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response.get_status())
        self.assertNotEqual(200, response.status_code)
        self.assertIn("token", response.get_message().lower())

    def test_stamp_invalid_email_format(self):
        stamp = StampV4(self.url, self.token)
        xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()

        headers = {
            "customid": self.generate_custom_id("STP"),
            "email": "correo_invalido"
        }

        response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response.get_status())
        self.assertNotEqual(200, response.status_code)
        self.assertIn("email", response.get_message().lower())

    def test_issue_duplicate_custom_id(self):
        issue = IssueV4(self.url, self.token)
        xml_content = self.update_date_xml("Test/resources/xml40.xml")

        headers = {
            "customid": self.generate_custom_id("ISS")
        }

        response1 = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("success", response1.get_status())
        self.assertEqual(200, response1.status_code)
        self.assertIsNotNone(response1.data.get("uuid"))

        response2 = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response2.get_status())
        self.assertIn("307", response2.get_message())

    def test_issue_json_invalid_format(self):
        issue = IssueV4(self.url, self.token)

        headers = {
            "customid": self.generate_custom_id("ISJ")
        }

        response = issue.issue_json('{"invalid": "json format for cfdi"}', headers=headers, version=ResponseVersion.V4)

        self.assertEqual("error", response.get_status())
        self.assertNotEqual(200, response.status_code)
        self.assertIsNotNone(response.get_message(), "El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestV4Basic)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
