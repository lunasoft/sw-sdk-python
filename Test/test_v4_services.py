import unittest
import os
import sys
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
import random
import string
import time
from typing import Union

PROJECT_ROOT = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, PROJECT_ROOT)

from Issue.IssueV4 import IssueV4
from Stamp.StampV4 import StampV4
from Utils.response_version import ResponseVersion

class TestV4Basic(unittest.TestCase):
    """
    Pruebas básicas para los servicios V4 de CFDI.
    Se prueban escenarios de éxito y error para Issue y Stamp.
    """
    
    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        self.url = "http://services.test.sw.com.mx"
        self.user = os.environ.get("SDKTEST_USER")
        self.password = os.environ.get("SDKTEST_PASSWORD")
        self.token = os.environ.get("SDKTEST_TOKEN")
        
        if not all([self.user, self.password, self.token]):
            raise ValueError("Faltan variables de entorno necesarias: SDKTEST_USER, SDKTEST_PASSWORD, SDKTEST_TOKEN")
    
    @staticmethod
    def generate_custom_id(prefix):
        """Genera un customId único usando un prefijo y caracteres aleatorios"""
        # Genera 4 caracteres aleatorios (2 letras y 2 números)
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=2))
        timestamp = datetime.now().strftime("%H%M")
        return f"{prefix}-{letters}{numbers}-{timestamp}"
    
    @staticmethod
    def update_date_xml(path_xml):
        """Actualiza la fecha en un archivo XML a la hora actual menos 1 hora"""
        try:
            ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}
            tree = ET.parse(path_xml)
            root = tree.getroot()
            
            new_date = datetime.now() - timedelta(hours=1)
            if "Fecha" in root.attrib:
                root.set("Fecha", new_date.strftime("%Y-%m-%dT%H:%M:%S"))
                ET.register_namespace("cfdi", ns["cfdi"]) 
                xml_buffer = BytesIO()
                tree.write(xml_buffer, encoding="utf-8", xml_declaration=True)
                return xml_buffer.getvalue().decode("utf-8")
            else:
                raise ValueError("No se encontró el atributo 'Fecha' en el XML")
        except Exception as e:
            raise

    # ============= CASOS DE ÉXITO =============

    def test_issue_xml_auth_all_headers(self):
        """Escenario 1: Issue XML exitoso con autenticación por credenciales y todos los headers"""
        try:
            issue = IssueV4(self.url, None, self.user, self.password)
            xml_content = self.update_date_xml("Test/resources/xml40.xml")
            
            headers = {
                "customid": self.generate_custom_id("ISS"),
                "email": "test1@test.com,test2@test.com",
                "pdf": "true"
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("success", response.get_status())
            self.assertIsNotNone(response.data)
            self.assertIsNotNone(response.data.get("cfdi")) #Dato de version 4
            self.assertIsNotNone(response.data.get("uuid")) #Dato de version 4 - UUID del comprobante
            self.assertEqual(200, response.status_code)
        except Exception as e:
            raise

    def test_issue_xml_token_minimal_headers(self):
        """Escenario 2: Issue XML exitoso con token y solo customId"""
        try:
            issue = IssueV4(self.url, self.token)
            xml_content = self.update_date_xml("Test/resources/xml40.xml")
            
            headers = {
                "customid": self.generate_custom_id("ISS")
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V3)
            
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data.get("cfdi")) #Dato de version 3
        except Exception as e:
            raise

    def test_stamp_token_all_headers(self):
        """Escenario 3: Stamp exitoso con token y todos los headers"""
        try:
            stamp = StampV4(self.url, self.token)
            xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()
            
            headers = {
                "customid": self.generate_custom_id("STP"),
                "email": "stamp1@test.com,stamp2@test.com",
                "pdf": "true"
            }
            
            response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V2)
            
            if response.get_status() == "error":
                self.assertIn("307", response.get_message())
                self.assertIn("timbre previo", response.get_message().lower())
            else:
                self.assertEqual("success", response.get_status())
                self.assertEqual(200, response.status_code)
                self.assertIsNotNone(response.data.get("tfd")) #Dato de version 2
        except Exception as e:
            raise

    def test_stamp_auth_email_only(self):
        """Escenario 4: Stamp exitoso con credenciales y solo email"""
        try:
            stamp = StampV4(self.url, None, self.user, self.password)
            xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()
            
            headers = {
                "email": "stamp1@test.com"
            }
            
            response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)
            
            if response.get_status() == "error":
                self.assertIn("307", response.get_message())
                self.assertIn("timbre previo", response.get_message().lower())
            else:
                self.assertEqual("success", response.get_status())
                self.assertEqual(200, response.status_code)
        except Exception as e:
            raise

    def test_issue_json_auth_all_headers(self):
        """Escenario 5: Issue JSON exitoso con autenticación y todos los headers"""
        try:
            issue = IssueV4(self.url, None, self.user, self.password)
            json_content = self.update_date_json("Test/resources/cfdi.json")
            
            headers = {
                "customid": self.generate_custom_id("ISJ"),
                "email": "test1@test.com,test2@test.com",
                "pdf": "true"
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("success", response.get_status())
            self.assertIsNotNone(response.data)
            self.assertIsNotNone(response.data.get("cfdi")) #Dato de version 4
            self.assertIsNotNone(response.data.get("uuid")) #Dato de version 4 - UUID del comprobante
            self.assertEqual(200, response.status_code)
        except Exception as e:
            raise

    def test_issue_json_token_minimal_headers(self):
        """Escenario 6: Issue JSON exitoso con token y solo customId usando V3"""
        try:
            issue = IssueV4(self.url, self.token)
            time.sleep(5)
            json_content = self.update_date_json("Test/resources/cfdi.json")
            
            headers = {
                "customid": self.generate_custom_id("ISJ")
            }
           
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V3)
            
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data.get("cfdi")) #Dato de version 3
        except Exception as e:
            raise

    def test_issue_json_with_pdf(self):
        """Escenario 7: Issue JSON exitoso validando respuesta con PDF"""
        try:
            issue = IssueV4(self.url, self.token)
            time.sleep(5)
            json_content = self.update_date_json("Test/resources/cfdi.json")
            
            headers = {
                "customid": self.generate_custom_id("ISJ"),
                "pdf": "true",
                "email": "test1@test.com"
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("success", response.get_status())
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data)
            self.assertIsNotNone(response.data.get("cfdi")) #Dato de version 4
            self.assertIsNotNone(response.data.get("uuid")) #Dato de version 4 - UUID del comprobante
        except Exception as e:
            raise

    # ============= CASOS DE ERROR =============

    def test_issue_xml_invalid_credentials(self):
        """Error 1: Issue XML con credenciales inválidas"""
        try:
            issue = IssueV4(self.url, None, "usuario_invalido", "pass_invalido")
            xml_content = self.update_date_xml("Test/resources/xml40.xml")
            
            headers = {
                "customid": self.generate_custom_id("ISS")
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response.get_status())
            self.assertNotEqual(200, response.status_code)
            self.assertIsNone(response.data)
            self.assertEqual("AU4101 - El token proporcionado viene vacio.", response.get_message())
        except Exception as e:
            raise

    def test_issue_xml_invalid_xml(self):
        """Error 2: Issue XML con XML mal formado o sin certificado"""
        try:
            issue = IssueV4(self.url, self.token)
            xml_content = "<xml>mal formado</xml>"
            
            headers = {
                "customid": self.generate_custom_id("ISS")
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response.get_status())
            self.assertNotEqual(200, response.status_code)
            self.assertIsNotNone(response.get_message)
        except Exception as e:
            raise

    def test_stamp_invalid_token(self):
        """Error 3: Stamp con token inválido"""
        try:
            stamp = StampV4(self.url, "token_invalido")
            xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()
            
            headers = {
                "customid": self.generate_custom_id("STP")
            }
            
            response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response.get_status())
            self.assertEqual("El token debe contener 3 partes", response.get_message())
            self.assertNotEqual(200, response.status_code)
        except Exception as e:
            raise

    def test_stamp_invalid_email_format(self):
        """Error 4: Stamp con formato de email inválido"""
        try:
            stamp = StampV4(self.url, self.token)
            xml_content = open("Test/resources/xml40Stamp.xml", "r", encoding='utf-8').read()
            
            headers = {
                "customid": self.generate_custom_id("STP"),
                "email": "correo_invalido"
            }
            
            response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response.get_status())
            self.assertNotEqual(200, response.status_code)
            self.assertEqual("El header email no tiene un correo válido (email).", response.get_message())
        except Exception as e:
            raise

    def test_issue_duplicate_custom_id(self):
        """Error 5: Issue - Error al intentar usar un customId duplicado"""
        try:
            issue = IssueV4(self.url, self.token)
            xml_content = self.update_date_xml("Test/resources/xml40.xml")
            
            custom_id = self.generate_custom_id("ISS")
            headers = {
                "customid": custom_id
            }
            
            response1 = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("success", response1.get_status())
            self.assertIsNotNone(response1.data.get("cfdi")) #Dato de version 4
            self.assertIsNotNone(response1.data.get("uuid")) #Dato de version 4 - UUID del comprobante
            self.assertEqual(200, response1.status_code)
            
            response2 = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response2.get_status())
            self.assertEqual("307. El comprobante contiene un timbre previo.", response2.get_message())
        except Exception as e:
            raise

    def test_issue_json_invalid_format(self):
        """Error 6: Issue JSON con formato inválido"""
        try:
            issue = IssueV4(self.url, self.token)
            json_content = '{"invalid": "json format for cfdi"}'
            
            headers = {
                "customid": self.generate_custom_id("ISJ")
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)
            
            self.assertEqual("error", response.get_status())
            self.assertNotEqual(200, response.status_code)
            self.assertIsNotNone(response.get_message())
        except Exception as e:
            raise

    @staticmethod
    def update_date_json(path_json):
        """Actualiza la fecha en un archivo JSON a la hora actual menos 1 hora"""
        try:
            with open(path_json, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            new_date = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
            if "Fecha" in data:
                data["Fecha"] = new_date
                return json.dumps(data, indent=2, ensure_ascii=False)
            else:
                raise ValueError("No se encontró la clave 'Fecha' en el JSON")
        except Exception as e:
            raise

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestV4Basic)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(not result.wasSuccessful())
    except Exception as e:
        sys.exit(1) 