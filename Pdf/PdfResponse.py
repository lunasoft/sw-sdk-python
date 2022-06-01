import json
from Utils.response import Response

class PdfResponse(Response):
    uuid = None
    pdf_b64 = None
    size_bytes = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            self.response = json.loads(response.text)
            self.data = self.response["data"]
            self.uuid = self.data["uuid"]
            self.pdf_b64 = self.data["contentB64"]
            self.size_bytes = self.response["contentSizeBytes"]
            self.status = self.response["status"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]

    def getUuid(self):
        return self.uuid

    def getPdfB64(self):
        return self.pdf_b64

    def getSizeBytes(self):
        return self.size_bytes