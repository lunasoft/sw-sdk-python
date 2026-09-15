import json
from Utils.response import Response

class StatusCfdiResponse:
    status_code = None
    response = None
    status_code_sat = None
    is_cancelable = None
    state = None
    cancelation_status = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            self.response = response.text
            self.status_code_sat = self.search_status_code_sat(self.response)
            self.is_cancelable = self.search_is_cancelable(self.response)
            self.state = self.search_state(self.response)
            self.cancelation_status = self.search_cancelation_status(self.response)
        except:
            self.status_code = response.status_code
    def search_status_code_sat(self, response):
        string = response.split("<a:CodigoEstatus>", 2)
        string2 = string[1].split("</a:CodigoEstatus>", 2)
        return string2[0]

    def search_is_cancelable(self, response):
        string = response.split("<a:EsCancelable>", 2)
        string2 = string[1].split("</a:EsCancelable>", 2)
        return string2[0]

    def search_state(self, response):
        string = response.split("<a:Estado>", 2)
        string2 = string[1].split("</a:Estado>", 2)
        return string2[0]

    def search_cancelation_status(self, response):
        string = response.split("<a:EstatusCancelacion>", 2)
        string2 = string[1].split("</a:EstatusCancelacion>", 2)
        return string2[0]
        
    def get_status_code(self):
        return self.status_code

    def get_response(self):
        return self.response

    def get_status_code_sat(self):
        return self.status_code_sat

    def get_is_cancelable(self):
        return self.is_cancelable

    def get_state(self):
        return self.state

    def get_cancelation_status(self):
        return self.cancelation_status