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
        """Consulta el saldo de timbres de la cuenta autenticada."""
        return BalanceRequest.account_balance(self.urlApi, self.get_token())

    def get_balance_by_id(self, idUser):
        """Consulta el saldo de timbres de una cuenta hija a partir de su identificador."""
        return BalanceRequest.account_balance_by_id(self.urlApi, self.get_token(), idUser)

    def add_stamps(self, userId, stamps, comment):
        """Asigna timbres a una cuenta hija desde la cuenta distribuidora."""
        return BalanceRequest.stamp_distribution(self.urlApi, self.get_token(), userId, stamps, comment,"Add")

    def remove_stamps(self, userId, stamps, comment):
        """Remueve timbres de una cuenta hija desde la cuenta distribuidora."""
        return BalanceRequest.stamp_distribution(self.urlApi, self.get_token(), userId, stamps, comment,"Remove")