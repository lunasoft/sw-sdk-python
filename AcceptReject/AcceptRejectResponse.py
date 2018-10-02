import json
from Utils.Response import Response
class AcceptRejectResponse(Response):
    codStatus = None
    folios = None
    acuse = None
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.acuse = self.response["acuse"]
            self.status = self.response["status"]
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]

    def getCodStatus(self):
        return self.codStatus
    def getFolios(self):
        return self.folios
    def getAcuse(self):
        return self.acuse