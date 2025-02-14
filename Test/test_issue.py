import unittest
import os
import json
import sys
from datetime import datetime, timedelta, UTC
import xml.etree.ElementTree as ET
from io import BytesIO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Issue.Issue import Issue

class TestIssue(unittest.TestCase):
    expected = "success"
    
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    @staticmethod
    def update_date_xml(path_xml):
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
            print("No se encontró el atributo 'Fecha' en el XML.")
            
    @staticmethod
    def update_date_json(path_json):
        with open(path_json, "r", encoding="utf-8") as file:
            data = json.load(file)
        new_date = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        if "Fecha" in data:
            data["Fecha"] = new_date
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            print("No se encontró la clave 'Fecha' en el JSON.")
        
    def testIssue(self):
        xml_path = self.update_date_xml("Test/resources/xml40.xml")
        issue = Issue("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = issue.issue_v4(xml_path)
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
                   
    def testIssueJson(self):
        json_path = self.update_date_json("Test/resources/cfdi.json")
        issue = Issue("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = issue.issue_json_v4(json_path)
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestIssue)
unittest.TextTestRunner(verbosity=2).run(suite)
