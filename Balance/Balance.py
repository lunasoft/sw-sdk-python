from Balance.BalanceRequest import BalanceRequest
from Utils.Services import Services

class Balance(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Balance, self).__init__(url, token, user, password)
    
    def account_balance(self):
        return BalanceRequest.account_balance(self.get_url(), self.get_token())
