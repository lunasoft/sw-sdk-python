import json
from Utils.Response import Response

class PendingsResponse(Response):
    UUID = None
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            try:
                self.UUID = self.data["UUID"]
                self.status = self.response["status"]
            except:
                self.status = self.response["status"]
            
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]

    def getUUIDs(self):
        return self.UUID