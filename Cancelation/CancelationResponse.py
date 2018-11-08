import json
import traceback
from Utils.Response import Response
class CancelationResponse(Response):
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            if(bool(cResponse.text and cResponse.text.strip())):
                self.response = json.loads(cResponse.text)
                if(self.statusCode == 200):
                    self.status = self.response["status"]
                    self.data = self.response["data"]
                else:
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = cResponse.reason
                self.messageDetail = cResponse.request
        except:
            traceback.print_exc()