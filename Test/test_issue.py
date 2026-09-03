import unittest
import os
import json
import sys
from datetime import datetime, timedelta, UTC
import xml.etree.ElementTree as ET
from io import BytesIO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from base64 import b64encode

from Issue.Issue import Issue

class TestIssue(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    #El servicio contesta este codigo cuando el comprobante ya tiene un timbre.
    codeStamped = "307"
    
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
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
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
        
    def testIssue_auth(self):
        xml = self.update_date_xml("Test/resources/xml40.xml")
        issue = Issue(self.url, None, self.user, self.password)
        response = issue.issue_v4(xml)
        self.assertEmision(response)

    def testIssue(self):
        xml = self.update_date_xml("Test/resources/xml40.xml")
        issue = Issue(self.url, self.token)
        response = issue.issue_v4(xml)
        self.assertEmision(response)

    def testIssue_b64(self):
        #El servicio tambien acepta el XML en base 64.
        xml = self.update_date_xml("Test/resources/xml40.xml")
        issue = Issue(self.url, self.token)
        response = issue.issue_v4(b64encode(xml.encode("utf-8")).decode("utf-8"), True)
        self.assertEmision(response)

    def testIssueJson_auth(self):
        json_content = self.update_date_json("Test/resources/cfdi.json")
        issue = Issue(self.url, None, self.user, self.password)
        response = issue.issue_json_v4(json_content)
        self.assertEmision(response)

    def testIssueJson(self):
        json_content = self.update_date_json("Test/resources/cfdi.json")
        issue = Issue(self.url, self.token)
        response = issue.issue_json_v4(json_content)
        self.assertEmision(response)

    #UT de Error
    def testIssue_invalidXml(self):
        issue = Issue(self.url, self.token)
        response = issue.issue_v4("<xml>no es un cfdi</xml>")
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testIssue_invalidToken(self):
        issue = Issue(self.url, "token-invalido")
        response = issue.issue_v4(self.update_date_xml("Test/resources/xml40.xml"))
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def assertEmision(self, response):
        #Reemitir el mismo comprobante responde con el timbre previo, y es un
        #resultado valido para la prueba.
        if response.get_status() == self.expectedError:
            self.assertIn(self.codeStamped, response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())
            self.assertIsNotNone(response.get_data())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIssue)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
