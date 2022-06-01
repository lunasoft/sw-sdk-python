from StatusCfdi.StatusCfdiRequest import StatusCfdiRequest
from Utils.Services import Services

class StatusCfdi:
    @staticmethod
    def status(rfc_emisor, rfc_receptor, total, uuid, url, action):
        return StatusCfdiRequest.status(rfc_emisor, rfc_receptor, total, uuid, url, action)