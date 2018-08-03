import json
from Utils.Response import Response#Package.File import class
class CancelationResponse(Response):
    def __init__(self, cResponse):
        try:
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.status = self.response["status"]
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]