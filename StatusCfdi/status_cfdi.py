from StatusCfdi.status_cfdi_request import StatusCfdiRequest
from Utils.services import Services

class StatusCfdi:
    @staticmethod
    def status(rfc_emisor, rfc_receptor, total, uuid, url, action):
        return StatusCfdiRequest.status(rfc_emisor, rfc_receptor, total, uuid, url, action)