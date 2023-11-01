import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Balance.Balance import Balance


class TestBalance(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testBalance(self):
        balance = Balance("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = balance.account_balance()
        self.assertTrue(self.expected == response.get_status())
    
    

suite = unittest.TestLoader().loadTestsFromTestCase(TestBalance)
unittest.TextTestRunner(verbosity=2).run(suite)
