import requests
import string
import random
from Pdf.PdfResponse import PdfResponse

class PdfRequest:
    @staticmethod
    def generatePdf(url, token, xml, templateId = "3a12dabd-66fa-4f18-af09-d1efd77ae9ce", extras = None):
        lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
        boundary = "".join(lst)
        payload = "--" + boundary + "\r\nContent-Type: text/xml\r\nContent-Transfer-Encoding: binary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"xml\"\r\n\r\n" + str(xml) + "\r\n--" + boundary + "-- "
        headers = {
            'Authorization': "Bearer " + token,
            'Content-Type': "multipart/form-data; boundary=\"" + boundary + "\"",
            'TemplateId': '\"'+templateId+'\"'
        }
        response = requests.request("POST", url + "/pdf/v1/generate", data=payload, headers=headers)
        return PdfResponse(response)