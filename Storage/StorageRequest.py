from Storage.StorageResponse import StorageResponse
from Utils.requestHelper import RequestHelper

class StorageRequest:
    @staticmethod
    def get_by_uuid(urlApi, token, uuid):
        """Consulta un CFDI por su UUID. El formato del UUID no se valida en local:
        se envía tal cual y responde el servicio."""
        endpoint = f"{urlApi}/datawarehouse/v1/live/{str(uuid)}"
        response = RequestHelper.get_json_request(endpoint,token)
        return StorageResponse(response)
