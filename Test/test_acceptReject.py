import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from AcceptReject.AcceptReject import AcceptReject

class TestAcceptReject(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testAcceptRejectCsd_auth(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd("EKU9003173C9",uuids,TestAcceptReject.open_file("Test/resources/b64CSD.txt"), TestAcceptReject.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    
    def testAcceptRejectCsd(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd("EKU9003173C9",uuids,TestAcceptReject.open_file("Test/resources/b64CSD.txt"), TestAcceptReject.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectXml_auth(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = accept_reject.accept_reject_xml(TestAcceptReject.open_file("Test/resources/fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectXml(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = accept_reject.accept_reject_xml(TestAcceptReject.open_file("Test/resources/fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectPfx_auth(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx("EKU9003173C9",uuids,TestAcceptReject.open_file("Test/resources/b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectPfx(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx("EKU9003173C9",uuids,TestAcceptReject.open_file("Test/resources/b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectUuid_autth(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = accept_reject.accept_reject_uuid("EKU9003173C9","baf029f3-93ea-4267-a76c-1958d69bd4d8", "Rechazo")
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectUuid(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = accept_reject.accept_reject_uuid("EKU9003173C9","baf029f3-93ea-4267-a76c-1958d69bd4d8", "Rechazo")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(TestAcceptReject)
unittest.TextTestRunner(verbosity=2).run(suite)
