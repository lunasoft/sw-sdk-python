from Balance.BalanceResponse import BalanceResponse,AccountBalanceResponse
from Utils.requestHelper import RequestHelper

class BalanceRequest:
    @staticmethod
    def account_balance(url_api, token):
        """Consulta el saldo de timbres de la cuenta asociada al token."""
        endpoint = url_api + "/management/v2/api/users/balance"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def account_balance_by_id(url_api, token, idUser):
        """Consulta el saldo de timbres de una cuenta hija por su idUser."""
        endpoint = f"{url_api}/management/v2/api/dealers/balance/users/{idUser}"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)

    @staticmethod
    def add_stamps(url_api, token, userId, stamps, comment):
        """Asigna timbres a una cuenta hija."""
        endpoint = f"{url_api}/management/v2/api/dealers/users/{userId}/stamps"
        payload = {
            "stamps": stamps,
            "comment": comment
        }
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return AccountBalanceResponse(response)

    @staticmethod
    def remove_stamps(url_api, token, userId, stamps, comment):
        """Remueve timbres de una cuenta hija."""
        endpoint = f"{url_api}/management/v2/api/dealers/users/{userId}/stamps"
        payload = {
            "stamps": stamps,
            "comment": comment
        }
        response = RequestHelper.delete_json_request(endpoint, token, payload)
        return AccountBalanceResponse(response)
    