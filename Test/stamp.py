from Auth.Auth import Auth
from Stamp.Stamp import Stamp
import base64
import unittest

def open_file(pathFile):
    out = open(pathFile,"r", encoding='ansi', errors='ignore').read()
    return out
class MyTest(unittest.TestCase):
    def __init__(self):
        self.expected = "success"
        self.message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    def testStampb64(self):
        xml = open_file("resources\\xml33.xml")
        encoded = base64.b64encode(xml.encode('utf-8'))
        obj = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponse = obj.StampV4(encoded.decode(),True)
        self.assertTrue(self.message == objResponse.getMessage())
    def testStamp(self):
        xml = open_file("resources\\xml33.xml")
        obj = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        objResponse = obj.StampV4(xml)
        self.assertTrue(self.message == objResponse.getMessage())

Test = MyTest()
Test.testStampb64()
Test.testStamp()