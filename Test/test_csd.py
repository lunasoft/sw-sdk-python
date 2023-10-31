import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Csd.Csd import Csd

class MyTest(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, "david.reyes@sw.com.mx", "TEST2022")
        response = csd_obj.upload_csd("stamp", MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)
