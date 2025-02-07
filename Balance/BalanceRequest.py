from Balance.BalanceResponse import BalanceResponse
from Utils.requestHelper import RequestHelper

class BalanceRequest:
    @staticmethod
    def account_balance(url, token):
        endpoint = url + "/account/balance"
        response = RequestHelper.get_json_request(endpoint,token,None)
        return BalanceResponse(response)