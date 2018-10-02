
class Response:
    status = None
    statusCode = None
    message = None
    messageDetail = None
    data = None
    response = None
    def getStatus(self):
        return self.status
    def getMessage(self):
        return self.message
    def getMessageDetail(self):
        return self.messageDetail
    def getData(self):
        return self.data
    def getResponse(self):
        return self.response
    def getStatusCode(self):
        return self.statusCode