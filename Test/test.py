import unittest
import json
from auth.auth import Auth
from stamp.stamp import Stamp
from issue.issue import Issue
from balance.balance import Balance
from cancelation.cancelation import Cancelation
from validate.validate import Validate
from relations.relations import Relations
from accept_reject.accept_reject import AcceptReject
from pendings.pendings import Pendings
from status_cfdi.status_cfdi import StatusCfdi

def open_file(pathFile):
    out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
    return out

class MyTest(unittest.TestCase):
    def __init__(self):
        self.expected = "success"
        self.message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    def testAuth(self):
        objAuth = Auth("http://services.test.sw.com.mx", None ,"demo","123456789")
        objResponseAuth = objAuth.authentication()
        self.assertTrue(self.expected == objResponseAuth.get_status())
    def testStamp(self):
        objStamp = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseStamp = objStamp.stamp_v4(open_file("resources\\xml33.xml"))
        if objResponseStamp.get_status() == "error":
            self.assertTrue(self.message == objResponseStamp.get_message())
        else:
            self.assertTrue(self.expected == objResponseStamp.get_status())
    def testIssue(self):
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.issue_v4(open_file("resources\\xml33.xml"))
        if objResponseIssue.get_status() == "error":
            self.assertTrue(self.message == objResponseIssue.get_message())
        else:
            self.assertTrue(self.expected == objResponseIssue.get_status())
    def testIssueJson(self):
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.issue_json_v4(open_file("resources\\cfdi.json"))
        if objResponseIssue.get_status() == "error":
            self.assertTrue(self.message == objResponseIssue.get_message())
        else:
            self.assertTrue(self.expected == objResponseIssue.get_status())
    def testBalance(self):
        objBal = Balance("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseBal = objBal.account_balance()
        self.assertTrue(self.expected == objResponseBal.get_status())
    def testCancelXml(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelXML = objCancel.cancel_xml(open_file("resources\\cancelByXml.xml"))
        self.assertTrue(self.expected == objResponseCancelXML.get_status())
    def testCancelCsd(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelCSD = objCancel.cancel_csd("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",open_file("resources\\b64CSD.txt"), open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseCancelCSD.get_status())
    def testCancelPfx(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelPFX = objCancel.cancel_pfx("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseCancelPFX.get_status())
    def testCancelUuid(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelUUID = objCancel.cancel_uuid("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207")
        self.assertTrue(self.expected == objResponseCancelUUID.get_status())
    def testValidateXml(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateXml = objValidate.validate_xml(open_file("resources\\xml33.xml"))
        self.assertTrue(self.expected == objResponseValidateXml.get_status())
    def testValidateLco(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateNoCert = objValidate.validate_lco("20001000000300022815")
        self.assertTrue(self.expected == objResponseValidateNoCert.get_status())
    def testValidateLrfc(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateRFC = objValidate.validate_lrfc("LAN7008173R5")
        self.assertTrue(self.expected == objResponseValidateRFC.get_status())
    def testRelationsCsd(self):
        objrelations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseRelations = objrelations.relations_csd("LAN7008173R5","a618ea43-28a8-48b6-8f2a-6c8c6702445c",open_file("resources\\b64CSD.txt"), open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseRelations.get_status())
    def testRelationsXml(self):
        objrelations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseRelations = objrelations.relations_xml(open_file("resources\\fileRelations.xml"))
        self.assertTrue(self.expected == objResponseRelations.get_status())
    def testRelationsPfx(self):
        objrelations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseRelations = objrelations.relations_pfx("LAN7008173R5","a618ea43-28a8-48b6-8f2a-6c8c6702445c",open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseRelations.get_status())
    def testRelationsUuid(self):
        objrelations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseRelations = objrelations.relations_uuid("LAN7008173R5","a618ea43-28a8-48b6-8f2a-6c8c6702445c")
        self.assertTrue(self.expected == objResponseRelations.get_status())
    def testAcceptRejectCsd(self):
        objAcceptReject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        objResponseAcceptRejectCSD = objAcceptReject.accept_reject_csd("LAN7008173R5",uuids,open_file("resources\\b64CSD.txt"), open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseAcceptRejectCSD.get_status())
    def testAcceptRejectXml(self):
        objAcceptReject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseAcceptRejectXml = objAcceptReject.accept_reject_xml(open_file("resources\\fileAcceptReject.xml"))
        self.assertTrue(self.expected == objResponseAcceptRejectXml.get_status())
    def testAcceptRejectPfx(self):
        objAcceptReject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        uuids = [{"uuid":"baf029f3-93ea-4267-a76c-1958d69bd4d8", "action":"Rechazo"}]
        objResponseAcceptRejectPFX = objAcceptReject.accept_reject_pfx("LAN7008173R5",uuids,open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseAcceptRejectPFX.get_status())
    def testAcceptRejectUuid(self):
        objAcceptReject = AcceptReject("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseAcceptRejectUUID = objAcceptReject.accept_reject_uuid("LAN7008173R5","baf029f3-93ea-4267-a76c-1958d69bd4d8", "Rechazo")
        self.assertTrue(self.expected == objResponseAcceptRejectUUID.get_status())
    def testPendings(self):
        objPendings = Pendings("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponse = objPendings.pendings("LAN7008173R5")
        self.assertTrue(self.expected == objResponse.get_status())
    def testStatusCfdi(self):
        objStatus = StatusCfdi.status("LAN8507268IA", "LAN7008173R5", "5800.00", "eb978000-95c7-4513-8d97-4b59434da45f", "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
        self.assertTrue(objStatus.statusCode==200)

Test = MyTest()
Test.testAuth()
Test.testStamp()
Test.testIssue()
Test.testIssueJson()
Test.testBalance()
Test.testCancelXml()
Test.testCancelCsd()
Test.testCancelPfx()
Test.testCancelUuid()
Test.testValidateXml()
Test.testValidateLco()
Test.testValidateLrfc()
Test.testRelationsCsd()
Test.testRelationsPfx()
Test.testRelationsXml()
Test.testRelationsUuid()
Test.testAcceptRejectCsd()
Test.testAcceptRejectPfx()
Test.testAcceptRejectXml()
Test.testAcceptRejectUuid()
Test.testPendings()
Test.testStatusCfdi()