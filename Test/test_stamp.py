from Stamp.Stamp import Stamp
import base64
import unittest

class TestStamp(unittest.TestCase):
    expected = "success"
    message = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='latin_1', errors='ignore').read()
        return out
    def test_stamp_b64(self):
        xml = TestStamp.open_file("resources/xml33.xml")
        encoded = base64.b64encode(xml.encode('utf-8'))
        stamp = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = stamp.stamp_v4(encoded.decode(),True)
        self.assertTrue(self.message == response.get_message())
    def test_stamp(self):
        xml = TestStamp.open_file("resources/xml33.xml")
        stamp = Stamp("http://services.test.sw.com.mx", None, "demo", "123456789")
        response = stamp.stamp_v4(xml)
        self.assertTrue(self.message == response.get_message())

suite = unittest.TestLoader().loadTestsFromTestCase(TestStamp)
unittest.TextTestRunner(verbosity=2).run(suite)