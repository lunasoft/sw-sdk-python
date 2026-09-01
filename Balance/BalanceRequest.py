from Balance.BalanceResponse import BalanceResponse,AccountBalanceResponse
from Utils.requestHelper import RequestHelper

class BalanceRequest:
    @staticmethod
    def account_balance(urlApi, token):
        """Arma la consulta del saldo de la cuenta autenticada."""
        endpoint = urlApi + "/management/v2/api/users/balance"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def account_balance_by_id(urlApi, token, idUser):
        """Arma la consulta del saldo de una cuenta hija a partir de su identificador."""
        endpoint = f"{urlApi}/management/v2/api/dealers/balance/users/{idUser}"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def stamp_distribution(urlApi, token, userId, stamps, comment,action):
        """Arma la asignación o la remoción de timbres de una cuenta hija."""
        endpoint = f"{urlApi}/management/v2/api/dealers/users/{userId}/stamps"
        payload = {
            "stamps": stamps,
            "comment": comment
        }
        if action == "Add":
            response = RequestHelper.post_json_request(endpoint,token,payload)
        elif action == "Remove":
            response = RequestHelper.delete_json_request(endpoint, token, payload)
        return AccountBalanceResponse(response)
    