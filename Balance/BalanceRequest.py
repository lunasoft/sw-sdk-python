from Balance.BalanceResponse import BalanceResponse,AccountBalanceResponse
from Utils.requestHelper import RequestHelper

class BalanceRequest:
    @staticmethod
    def account_balance(urlApi, token):
        """Consulta el saldo de timbres de la cuenta asociada al token."""
        endpoint = urlApi + "/management/v2/api/users/balance"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def account_balance_by_id(urlApi, token, idUser):
        """Consulta el saldo de timbres de una cuenta hija por su idUser."""
        endpoint = f"{urlApi}/management/v2/api/dealers/balance/users/{idUser}"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def stamp_distribution(urlApi, token, userId, stamps, comment,action):
        """Asigna o remueve timbres de una cuenta hija."""
        endpoint = f"{urlApi}/management/v2/api/dealers/users/{userId}/stamps"
        payload = {
            "stamps": stamps,
            "comment": comment
        }
        if action == "Add":
            response = RequestHelper.post_json_request(endpoint,token,payload)
        else:
            response = RequestHelper.delete_json_request(endpoint, token, payload)
        return AccountBalanceResponse(response)
    