import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Cancelation.Cancelation import Cancelation


class TestCancelation(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testCancelXml_Auth(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelXml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelXml(self):
        cancel = Cancelation("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelXml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelCsd_Auth(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelCsd("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelCsd(self):
        cancel = Cancelation("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelCsd("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelPfx_Auth(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelPfx("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", TestCancelation.open_file("Test/resources/b64PFX.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelPfx(self):
        cancel = Cancelation("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelPfx("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", TestCancelation.open_file("Test/resources/b64PFX.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid_Auth(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelUuid("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid(self):
        cancel = Cancelation("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelUuid("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", "02", "")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelation)
unittest.TextTestRunner(verbosity=2).run(suite)
