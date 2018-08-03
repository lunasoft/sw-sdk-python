import json
from Utils.Response import Response#Package.File import class

class StampResponse(Response):
    uuid = None
    qrCode = None
    cfdi = None
    def __init__(self,cResponse):
        try:
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.status = self.response["status"]
            self.uuid = self.data["uuid"]
            self.qrCode = self.data["qrCode"]
            self.cfdi = self.data["cfdi"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]

    def getUuid(self):
        return self.uuid

    def getQrCode(self):
        return self.qrCode

    def getCfdi(self):
        return self.cfdi