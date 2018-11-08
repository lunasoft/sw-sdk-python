import json
import traceback
from Utils.Response import Response

class BalanceResponse(Response):
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            if(bool(cResponse.text and cResponse.text.strip())):
                self.response = json.loads(cResponse.text)
                if(self.statusCode == 200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                else:
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = cResponse.reason
                self.messageDetail = cResponse.request
        except:
            traceback.print_exc()