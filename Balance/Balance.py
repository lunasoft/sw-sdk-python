from balance.balance_request import BalanceRequest
from utils.services import Services

class Balance(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Balance, self).__init__(url, token, user, password)
    
    def account_balance(self):
        return BalanceRequest.account_balance(self.url, self.token)