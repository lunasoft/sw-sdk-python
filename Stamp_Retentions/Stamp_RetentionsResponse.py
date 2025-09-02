import json
import traceback
from Utils.response import Response

class Stamp_RetentionsResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                else:
                    # Some error responses may not include status
                    self.status = self.response.get("status", "error")
                    self.message = self.response.get("message")
                    if "messageDetail" in self.response:
                        self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()


