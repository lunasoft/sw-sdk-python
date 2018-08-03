import unittest
from Auth.Auth import Auth
from Stamp.Stamp import Stamp
from Issue.Issue import Issue
from Balance.Balance import Balance
from Cancelation.Cancelation import Cancelation
from Validate.Validate import Validate
import os
os.chdir("C:\\out\\Python\\SW_SDK_Python")#path to proyect, to use relative paths to resources

def open_file(pathFile):
    out = open(pathFile,"r", encoding='ansi', errors='ignore').read()
    return out

class MyTest(unittest.TestCase):
    def __init__(self):
        self.expected = "success"
        self.message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."

    def testAuth(self):
        objAuth = Auth("http://services.test.sw.com.mx", None ,"demo","123456789")
        objResponseAuth = objAuth.Authentication() 
        self.assertTrue(self.expected == objResponseAuth.getStatus())
    def testStamp(self):
        objStamp = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseStamp = objStamp.StampV4(open_file("resources\\xml33.xml"))
        if objResponseStamp.getStatus() == "error":
            self.assertTrue(self.message == objResponseStamp.getMessage())
        else:
            self.assertTrue(self.expected == objResponseStamp.getStatus())
    def testIssue(self):
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.IssueV4(open_file("resources\\xml33.xml"))
        if objResponseIssue.getStatus() == "error":
            self.assertTrue(self.message == objResponseIssue.getMessage())
        else:
            self.assertTrue(self.expected == objResponseIssue.getStatus())
    def testBalance(self):
        objBal = Balance("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseBal = objBal.AccountBalance()
        self.assertTrue(self.expected == objResponseBal.getStatus())
    def testCancelXml(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelXML = objCancel.CancelXml(open_file("resources\\cancelByXml.xml"))
        self.assertTrue(self.expected == objResponseCancelXML.getStatus())
    def testCancelCsd(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelCSD = objCancel.CancelCsd("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",open_file("resources\\b64CSD.txt"), open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseCancelCSD.getStatus())
    def testCancelPfx(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelPFX = objCancel.CancelPfx("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207",open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == objResponseCancelPFX.getStatus())
    def testCancelUuid(self):
        objCancel = Cancelation("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseCancelUUID = objCancel.CancelUuid("LAN7008173R5","c846c65a-6371-4449-9db6-a7daca2f7207")
        self.assertTrue(self.expected == objResponseCancelUUID.getStatus())
    def testValidateXml(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateXml = objValidate.ValidateXml(open_file("resources\\xml33.xml"))
        self.assertTrue(self.expected == objResponseValidateXml.getStatus())
    def testValidateLco(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateNoCert = objValidate.ValidateLco("20001000000300022815")
        self.assertTrue(self.expected == objResponseValidateNoCert.getStatus())
    def testValidateLrfc(self):
        objValidate = Validate("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseValidateRFC = objValidate.ValidateLrfc("LAN7008173R5")
        self.assertTrue(self.expected == objResponseValidateRFC.getStatus())

Test = MyTest()
Test.testAuth()
Test.testStamp()
Test.testIssue()
Test.testBalance()
Test.testCancelXml()
Test.testCancelCsd()
Test.testCancelPfx()
Test.testCancelUuid()
Test.testValidateXml()
Test.testValidateLco()
Test.testValidateLrfc()