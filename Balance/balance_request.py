import requests
from balance.balance_response import BalanceResponse
class BalanceRequest:
    @staticmethod
    def account_balance(url, token):
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        response = requests.request("GET", url + "/account/balance", headers = headers, verify = True, timeout=300)
        return BalanceResponse(response)