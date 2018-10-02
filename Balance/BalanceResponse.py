import json
from Utils.Response import Response

class BalanceResponse(Response):
    def __init__(self, cResponse):
        try:
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.status = self.response["status"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]