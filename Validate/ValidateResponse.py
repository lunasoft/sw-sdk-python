import json
from Utils.Response import Response

class ValidateResponse(Response):
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.status = self.response["status"]
        except:
            try:
                self.message = self.response["message"]
                self.messageDetail = self.response["messageDetail"]
                self.status = self.response["status"]
            except:
                self.status = self.response["status"]