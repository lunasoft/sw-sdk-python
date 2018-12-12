from Issue.issue import Issue
import base64
import json
import datetime
import unittest

class TestIssue(unittest.TestCase):
    expected = "success"
    message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile,"r", encoding='latin_1', errors='ignore').read()
        return out
    def test_issue_b64(self):
        xml = TestIssue.open_file("resources/xml33.xml")
        encoded = base64.b64encode(xml.encode('utf-8'))
        issue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = issue.issue_v4(encoded.decode(),True)
        self.assertTrue(response.get_status() == self.expected or self.message == response.get_message())
    def test_issue(self):
        xml = TestIssue.open_file("resources/xml33.xml")
        issue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = issue.issue_v4(xml)
        self.assertTrue(response.get_status() == self.expected or self.message == response.get_message())
    def test_issue_json(self):
        jsontxt = TestIssue.open_file("resources/cfdi.json")
        JSON = json.loads(jsontxt)
        fecha = (datetime.datetime.now()-datetime.timedelta(days = 1)).strftime('%Y-%m-%dT%H:%M:%S')
        JSON['Fecha'] = fecha
        jsontxt = json.dumps(JSON)
        issue = Issue("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = issue.issue_json_v4(jsontxt)
        self.assertTrue(response.get_status() == self.expected or self.message == response.get_message())

suite = unittest.TestLoader().loadTestsFromTestCase(TestIssue)
unittest.TextTestRunner(verbosity=2).run(suite)