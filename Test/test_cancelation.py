import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Cancelation.Cancelation import Cancelation


class MyTest(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testCancelXml(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "david.reyes@sw.com.mx", "TEST2022")
        response = cancel.CancelXml(MyTest.open_file("resources\\cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelCsd(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "david.reyes@sw.com.mx", "TEST2022")
        response = cancel.CancelCsd("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelPfx(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "david.reyes@sw.com.mx", "TEST2022")
        response = cancel.CancelPfx("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", MyTest.open_file("resources\\b64PFX.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelUuid(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "david.reyes@sw.com.mx", "TEST2022")
        response = cancel.CancelUuid("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", "02", "")
        self.assertTrue(self.expected == response.get_status())
    

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)
