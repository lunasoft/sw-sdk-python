import unittest
import json
from Auth.Auth import Auth
from Stamp.Stamp import Stamp
from Issue.Issue import Issue
from Balance.Balance import Balance
from Cancelation.Cancelation import Cancelation
from Validate.Validate import Validate
from Relations.Relations import Relations
from AcceptReject.AcceptReject import AcceptReject
from Pendings.Pendings import Pendings
from StatusCfdi.StatusCfdi import StatusCfdi
from Csd.Csd import Csd

class MyTest(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testAuth(self):
        auth = Auth("http://services.test.sw.com.mx", None ,"userforut@ut.com", "swpassut")
        response = auth.authentication()
        self.assertTrue(self.expected == response.get_status())
    def testStamp(self):
        stamp = Stamp("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = stamp.stamp_v4(MyTest.open_file("resources\\xml40.xml"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testIssue(self):
        issue = Issue("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = issue.issue_v4(MyTest.open_file("resources\\xml40.xml"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testIssueJson(self):
        issue = Issue("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = issue.issue_json_v4(MyTest.open_file("resources\\cfdi.json"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testBalance(self):
        balance = Balance("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = balance.account_balance()
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelXml(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = cancel.CancelXml(MyTest.open_file("resources\\cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelCsd(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = cancel.CancelCsd("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelPfx(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = cancel.CancelPfx("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", MyTest.open_file("resources\\b64PFX.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    
    def testCancelUuid(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = cancel.CancelUuid("3dda215e-4c77-4923-94a1-627e0a04378c", "EKU9003173C9", "02", "")
        self.assertTrue(self.expected == response.get_status())
    def testValidateXml(self):
        validate = Validate("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = validate.ValidateXml(MyTest.open_file("resources\\xml40.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testRelationsCsd(self):
        relations = Relations("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = relations.relations_csd("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90",MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsPfx(self):
        relations = Relations("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = relations.relations_pfx("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90",MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsUuid(self):
        relations = Relations("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = relations.relations_uuid("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90")
        self.assertTrue(self.expected == response.get_status())
    def testPendings(self):
        pendings = Pendings("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expected == response.get_status())
    def testStatusCfdi(self):
        objStatus = StatusCfdi.status("EKU9003173C9", "EKU9003173C9", "100.00", "316dff4d-6a5a-40d5-8558-c8f45244aa90", "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
        self.assertTrue(objStatus.status_code == 200)
    def testAcceptRejectCsd(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd("EKU9003173C9",uuids,MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectXml(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = accept_reject.accept_reject_xml(MyTest.open_file("resources\\fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectPfx(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx("EKU9003173C9",uuids,MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectUuid(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = accept_reject.accept_reject_uuid("EKU9003173C9","baf029f3-93ea-4267-a76c-1958d69bd4d8", "Rechazo")
        self.assertTrue(self.expected == response.get_status())
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, "userforut@ut.com", "swpassut")
        response = csd_obj.upload_csd("stamp", MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)
