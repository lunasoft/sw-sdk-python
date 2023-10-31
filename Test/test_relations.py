import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)


from Relations.Relations import Relations


class MyTest(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testRelationsCsd(self):
        relations = Relations("http://services.test.sw.com.mx", None, os.environ["USER_EMAIL"], os.environ["SW_PASSWORD"])
        response = relations.relations_csd("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90",MyTest.open_file("resources\\b64CSD.txt"), MyTest.open_file("resources\\b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsPfx(self):
        relations = Relations("http://services.test.sw.com.mx", None, os.environ["USER_EMAIL"], os.environ["SW_PASSWORD"])
        response = relations.relations_pfx("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90",MyTest.open_file("resources\\b64PFX.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
    def testRelationsUuid(self):
        relations = Relations("http://services.test.sw.com.mx", None, os.environ["USER_EMAIL"], os.environ["SW_PASSWORD"])
        response = relations.relations_uuid("EKU9003173C9","316dff4d-6a5a-40d5-8558-c8f45244aa90")
        self.assertTrue(self.expected == response.get_status())
    

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)
