import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Stamp_Retentions.Stamp_Retentions import Stamp_Retentions


class TestStampRetentions(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    messageAuth = "401 - El rango de la fecha de generación no debe de ser mayor a 72 horas para la emisión del timbre."

    @staticmethod
    def open_file(pathFile):
        try:
            return open(pathFile, "r", encoding='utf-8').read()
        except UnicodeDecodeError:
            return open(pathFile, "r", encoding='utf-8').read()

    def testStampRetentions_xml(self):
        """Prueba timbrado con XML usando token"""
        print("\n=== Prueba: Timbrado con XML (token) ===")
        
        stamp = Stamp_Retentions("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        
        TestStampRetentions.log_response("xml", response)
        if response.get_status() == "error":
            self.assertTrue(self.message == response.get_message() or self.messageAuth == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())

    def testStampRetentions_xml_Error(self):
        """Prueba error timbrado con XML CFDI"""
        print("\n=== Prueba: Timbrado con XML (token) ===")

        stamp = Stamp_Retentions("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        xml_content = TestStampRetentions.open_file("Test/resources/xml40.xml")
        response = stamp.stamp_retetions_v3(xml_content)

        TestStampRetentions.log_response("xml", response)
        self.assertTrue(self.expected != response.get_status())

    def testStampRetentions_auth(self):
        """Prueba timbrado con autenticación de cuenta"""
        print("\n=== Prueba: Timbrado con auth ===")
        
        stamp = Stamp_Retentions(
            "https://services.test.sw.com.mx",
            None,
            os.environ["SDKTEST_USER"],
            os.environ["SDKTEST_PASSWORD"]
        )
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        
        TestStampRetentions.log_response("auth", response)
        if response.get_status() == "error":
              self.assertTrue(self.message == response.get_message() or self.messageAuth == response.get_message())
        else:
            self.assertTrue(self.expected == response.get_status())

    def testStampRetentions_authError(self):
        """Prueba error timbrado con autenticación de cuenta"""
        print("\n=== Prueba: Timbrado con auth ===")
        
        stamp = Stamp_Retentions(
            "https://services.test.sw.com.mx",
            None,
            "wrongUser",
            os.environ["SDKTEST_PASSWORD"]
        )
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        TestStampRetentions.log_response("auth", response)
        self.assertTrue(self.expected != response.get_status())

    @staticmethod
    def log_response(label, response):
        print(f"[{label}] status:", response.get_status())
        if response.get_status() == "error":
            print("message:", response.get_message())
            print("messageDetail:", response.get_messageDetail())
        else:
            data = response.get_data()
            if isinstance(data, dict) and "retencion" in data:
                xml = data["retencion"]
                print("retencion length:", len(xml))
                print("retencion head:", xml[:200])
            else:
                print("data:", data)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStampRetentions)
    unittest.TextTestRunner(verbosity=2).run(suite)


