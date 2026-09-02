from Balance.BalanceRequest import BalanceRequest
from Utils.Services import Services

class Balance(Services):
    urlApi = None
    def __init__(self, url, urlApi, token=None, user=None, password=None):
        super(Balance, self).__init__(url, token, user, password)
        if urlApi:
            self.urlApi = urlApi
        else: 
            print("Debe especificar la urlApi")
    
    def get_balance(self):
        return BalanceRequest.account_balance(self.urlApi, self.get_token())

    def get_balance_by_id(self, idUser):
        return BalanceRequest.account_balance_by_id(self.urlApi, self.get_token(), idUser)

    def add_stamps(self, userId, stamps, comment):
        return BalanceRequest.add_stamps(self.urlApi, self.get_token(), userId, stamps, comment)

    def remove_stamps(self, userId, stamps, comment):
        return BalanceRequest.remove_stamps(self.urlApi, self.get_token(), userId, stamps, comment)