from Utils.Services import Services
from AccountUser.AccountUserRequest import AccountUserRequest

class AccountUser(Services):
    urlApi = None
    def __init__(self, url, urlApi, token=None, user=None, password=None):
        super(AccountUser, self).__init__(url, token, user, password)
        if urlApi:
            self.urlApi = urlApi
        else: 
            print("Debe especificar la urlApi")
            
    def create_user(self,name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone):
        return AccountUserRequest.create_user(self.urlApi,self.get_token(),name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone)
    def delete_user(self,idUser):
        return AccountUserRequest.delete_user(self.urlApi,self.get_token(),idUser)
    def update_user(self,idUser,name,taxId,notificationEmail,phone,isUnlimited=False):
        return AccountUserRequest.update_user(self.urlApi,self.get_token(),idUser,name,taxId,notificationEmail,phone,isUnlimited)
    def getUser_all(self,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"All",page=page,perPage=perPage)
    def getUser_by_idUser(self,idUser,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"IdUser",idUser,page=page,perPage=perPage)
    def getUser_by_email(self, email,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"Email",None,email,page=page,perPage=perPage)
    def getUser_by_taxId(self, taxId,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"TaxId",None,None,taxId,page=page,perPage=perPage)
    def getUser_by_isActive(self, isActive,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"IsActive",None,None,None,isActive,page=page,perPage=perPage)
    def getUser_by_name(self, name,page=None,perPage=None):
        return AccountUserRequest.get_users(self.urlApi,self.get_token(),"Name",name=name,page=page,perPage=perPage)
