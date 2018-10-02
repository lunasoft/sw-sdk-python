from StatusCfdi.StatusCfdiRequest import StatusCfdiRequest
from Utils.Services import Services

class StatusCfdi:
    @staticmethod
    def status(cRFCEmisor, cRFCReceptor, cTotal, cUUID, cURL, cAction):
        return StatusCfdiRequest.status(cRFCEmisor, cRFCReceptor, cTotal, cUUID, cURL, cAction)