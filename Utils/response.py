
class Response:
    status = None
    status_code = None
    message = None
    messageDetail = None
    data = None
    response = None
    def get_status(self):
        return self.status
    def get_message(self):
        return self.message
    def get_messageDetail(self):
        return self.messageDetail
    def get_data(self):
        return self.data
    def get_response(self):
        return self.response
    def get_status_code(self):
        return self.status_code
