import json
from Utils.response import Response

class CancelationRetentionsResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    self.status = self.response["status"]
                    self.data = self.response["data"]
                else:
                    self.status = self.response.get("status", "error")
                    self.message = self.response.get("message")
                    if "messageDetail" in self.response: 
                        self.message_detail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.message_detail = response.request
        except Exception as error:
            self.set_unreadable(response, error)
