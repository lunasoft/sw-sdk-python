
class Response:
    status = None
    message = None
    messageDetail = None
    data = None

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getMessageDetail(self):
        return self.messageDetail

    def getData(self):
        return self.data