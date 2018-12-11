from status_cfdi.status_cfdi_request import StatusCfdiRequest
from utils.services import Services

class StatusCfdi:
    @staticmethod
    def status(rfc_emisor, rfc_receptor, total, uuid, url, action):
        return StatusCfdiRequest.status(rfc_emisor, rfc_receptor, total, uuid, url, action)