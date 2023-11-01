import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from StatusCfdi.StatusCfdi import StatusCfdi

class TestStatusCfdi(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testStatusCfdi(self):
        objStatus = StatusCfdi.status("EKU9003173C9", "EKU9003173C9", "100.00", "316dff4d-6a5a-40d5-8558-c8f45244aa90", "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
        self.assertTrue(objStatus.status_code == 200)

suite = unittest.TestLoader().loadTestsFromTestCase(TestStatusCfdi)
unittest.TextTestRunner(verbosity=2).run(suite)
