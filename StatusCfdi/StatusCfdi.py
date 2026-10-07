from StatusCfdi.StatusCfdiRequest import StatusCfdiRequest

class StatusCfdi:
    url = None
    def __init__(self, url):
        if not url:
            raise ValueError("Se debe definir URL")
        self.url = url

    def status(self, rfc_emisor, rfc_receptor, total, uuid):
        return StatusCfdiRequest.status(self.url, rfc_emisor, rfc_receptor, total, uuid)

    def get_url(self):
        return self.url
