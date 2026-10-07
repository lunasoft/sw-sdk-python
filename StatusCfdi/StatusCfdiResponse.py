import re
from Utils.response import Response

class StatusCfdiResponse(Response):
    status_code_sat = None
    is_cancelable = None
    state = None
    cancelation_status = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            self.response = response.text
            if(self.status_code == 200):
                self.status_code_sat = self.search_status_code_sat(self.response)
                if self.status_code_sat is None:
                    raise ValueError("La respuesta no trae CodigoEstatus")
                self.is_cancelable = self.search_is_cancelable(self.response)
                self.state = self.search_state(self.response)
                self.cancelation_status = self.search_cancelation_status(self.response)
                self.status = "success"
            else:
                self.status = "error"
                self.message = response.reason
                fault = re.search(r"<faultstring[^>]*>(.*?)</faultstring>", self.response, re.S)
                if fault:
                    self.message_detail = fault.group(1)
        except Exception as error:
            self.set_unreadable(response, error)

    @staticmethod
    def search(response, tag):
        #Un elemento ausente, vacío o con i:nil="true" queda en None.
        _, found, rest = response.partition(f"<a:{tag}>")
        if not found:
            return None
        return rest.partition(f"</a:{tag}>")[0] or None

    def search_status_code_sat(self, response):
        return self.search(response, "CodigoEstatus")

    def search_is_cancelable(self, response):
        return self.search(response, "EsCancelable")

    def search_state(self, response):
        return self.search(response, "Estado")

    def search_cancelation_status(self, response):
        return self.search(response, "EstatusCancelacion")

    def get_status_code_sat(self):
        return self.status_code_sat

    def get_is_cancelable(self):
        return self.is_cancelable

    def get_state(self):
        return self.state

    def get_cancelation_status(self):
        return self.cancelation_status
