
class Response:
    status = None
    status_code = None
    message = None
    message_detail = None
    data = None
    response = None
    def get_status(self):
        return self.status
    def get_message(self):
        return self.message
    def get_message_detail(self):
        return self.message_detail
    def get_data(self):
        return self.data
    def get_response(self):
        return self.response
    def get_status_code(self):
        return self.status_code

    def set_unreadable(self, response, error):
        #La respuesta no se pudo interpretar. Si ya se leyó el status del servicio se
        #respeta: un timbrado exitoso no debe reportarse como error y reintentarse.
        self.status = self.status or "error"
        if self.message is None:
            self.message = "No se pudo interpretar la respuesta del servicio"
            self.message_detail = f"{type(error).__name__}: {error}"
        if self.response is None:
            self.response = response.text
