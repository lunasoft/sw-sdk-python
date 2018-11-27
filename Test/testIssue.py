from Auth.Auth import Auth
from Issue.Issue import Issue
import base64
import unittest

def open_file(pathFile):
    out = open(pathFile,"r", encoding='latin_1', errors='ignore').read()
    return out
class MyTest(unittest.TestCase):
    def __init__(self):
        self.expected = "success"
        self.message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    def testIssueb64(self):
        xml = open_file("resources/xml33.xml")
        encoded = base64.b64encode(xml.encode('utf-8'))
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.IssueV4(encoded.decode(),True)
        self.assertTrue(self.message == objResponseIssue.getMessage())
    def testIssue(self):
        xml = open_file("resources/xml33.xml")
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.IssueV4(xml)
        self.assertTrue(self.message == objResponseIssue.getMessage())
    def testIssueJson(self):
        jsontxt = open_file("resources/cfdi.json")
        objIssue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponseIssue = objIssue.IssueJsonV4(jsontxt)
        self.assertTrue(self.message == objResponseIssue.getMessage())

Test = MyTest()
Test.testIssue()
Test.testIssueb64()
Test.testIssueJson()