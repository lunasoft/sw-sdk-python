import json
from Utils.Response import Response

class PdfResponse(Response):
    uuid = None
    pdfb64 = None
    sizeBytes = None
    def __init__(self,cResponse):
        try:
            self.statusCode = cResponse.status_code
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.uuid = self.data["uuid"]
            self.pdfb64 = self.data["contentB64"]
            self.sizeBytes = self.response["contentSizeBytes"]
            self.status = self.response["status"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]

    def getUuid(self):
        return self.uuid

    def getPdfB64(self):
        return self.pdfb64

    def getSizeBytes(self):
        return self.sizeBytes