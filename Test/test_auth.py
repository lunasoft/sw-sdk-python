import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Auth.Auth import Auth

class TestAuth(unittest.TestCase):
    expectedSucces = "success"
    expectedError = "error"
    
    def testAuth_success(self):
        auth = Auth("https://services.test.sw.com.mx", None , os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = auth.authentication()
        self.assertTrue(self.expectedSucces == response.get_status())
        self.assertIsNotNone(response.get_token(),"El valor de token esta vacio")
        
    def testAuth_emailError(self):
        auth = Auth("https://services.test.sw.com.mx", None , os.environ["SDKTEST_USER"], "wrongPassword")
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuth)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
