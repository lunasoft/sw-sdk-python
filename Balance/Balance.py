from Balance.BalanceRequest import BalanceRequest
from Utils.Services import Services

class Balance(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Balance,self).__init__(url, token, user, password)
    
    def AccountBalance(self):
        return BalanceRequest.account_balance(self.url, self.token)