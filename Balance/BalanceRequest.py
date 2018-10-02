import requests
from Balance.BalanceResponse import BalanceResponse
class BalanceRequest:
    @staticmethod
    def account_balance(url, token):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/account/balance", headers=headers)
        return BalanceResponse(response)