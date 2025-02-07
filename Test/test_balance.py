import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Balance.Balance import Balance

class TestBalance(unittest.TestCase):
    expected = "success"
    
    def testBalance_Auth(self):
        balance = Balance("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = balance.account_balance()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        
    def testBalance(self):
        balance = Balance("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = balance.account_balance()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())

suite = unittest.TestLoader().loadTestsFromTestCase(TestBalance)
unittest.TextTestRunner(verbosity=2).run(suite)
