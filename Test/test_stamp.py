import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Stamp.Stamp import Stamp


class TestStamp(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testStamp(self):
        stamp = Stamp("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = stamp.stamp_v4(TestStamp.open_file("resources\\xml40.xml"))
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())


suite = unittest.TestLoader().loadTestsFromTestCase(TestStamp)
unittest.TextTestRunner(verbosity=2).run(suite)
