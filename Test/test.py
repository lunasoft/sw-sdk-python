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
    message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testAuth(self):
        auth = Auth("http://services.test.sw.com.mx", None ,"demo","123456789")
        response = auth.authentication()
        self.assertTrue(self.expected == response.get_status())
    def testStamp(self):
        stamp = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = stamp.stamp_v4(MyTest.open_file("resources\\xml33.xml"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testIssue(self):
        issue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = issue.issue_v4(MyTest.open_file("resources\\xml33.xml"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testIssueJson(self):
        issue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = issue.issue_json_v4(MyTest.open_file("resources\\cfdi.json"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())
    def testBalance(self):
        balance = Balance("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = balance.account_balance()
        self.assertTrue(self.expected == response.get_status())
    def testCancelXml(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = cancel.cancel_xml(MyTest.open_file("resources\\cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testCancelCsd(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = cancel.cancel_csd("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testCancelPfx(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = cancel.cancel_pfx("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testCancelUuid(self):
        cancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = cancel.cancel_uuid("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207")
        self.assertTrue(self.expected == response.get_status())
    def testValidateXml(self):
        validate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = validate.validate_xml(MyTest.open_file("resources\\xml33.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testValidateLco(self):
        validate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = validate.validate_lco("20001000000300022815")
        self.assertTrue(self.expected == response.get_status())
    def testValidateLrfc(self):
        validate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = validate.validate_lrfc("LAN7008173R5")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsCsd(self):
        relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = relations.relations_csd("LAN7008173R5","a618ea43-28a8-48b6-8f2a-6c8c6702445c",MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsXml(self):
        relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = relations.relations_xml(MyTest.open_file("resources\\fileRelations.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testRelationsPfx(self):
        relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = relations.relations_pfx("LAN7008173R5","a618ea43-28a8-48b6-8f2a-6c8c6702445c",MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsUuid(self):
        relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = relations.relations_uuid("LAN7008173R5","4fb779d4-1ab5-4650-bf63-d46664d0009d")
        self.assertTrue(self.expected == response.get_status())
    def testPendings(self):
        pendings = Pendings("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = pendings.pendings("LAN7008173R5")
        self.assertTrue(self.expected == response.get_status())
    def testStatusCfdi(self):
        objStatus = StatusCfdi.status("LAN8507268IA", "LAN7008173R5", "5800.00", "eb978000-95c7-4513-8d97-4b59434da45f", "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
        self.assertTrue(objStatus.status_code == 200)
    def testAcceptRejectCsd(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd("LAN7008173R5",uuids,MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectXml(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = accept_reject.accept_reject_xml(MyTest.open_file("resources\\fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectPfx(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx("LAN7008173R5",uuids,MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testAcceptRejectUuid(self):
        accept_reject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = accept_reject.accept_reject_uuid("LAN7008173R5","baf029f3-93ea-4267-a76c-1958d69bd4d8", "Rechazo")
        self.assertTrue(self.expected == response.get_status())
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = csd_obj.upload_csd("stamp", MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)