from Utils.Services import Services
from AccountUser.AccountUserRequest import AccountUserRequest

class AccountUser(Services):
    url_api = None
    def __init__(self, url, url_api, token=None, user=None, password=None):
        super(AccountUser, self).__init__(url, token, user, password)
        if url_api:
            self.url_api = url_api
        else: 
            print("Debe especificar la url_api")
            
    def create_user(self,name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone):
        return AccountUserRequest.create_user(self.url_api,self.get_token(),name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone)
    def delete_user(self,idUser):
        return AccountUserRequest.delete_user(self.url_api,self.get_token(),idUser)
    def update_user(self,idUser,name,taxId,notificationEmail,phone,isUnlimited=False):
        return AccountUserRequest.update_user(self.url_api,self.get_token(),idUser,name,taxId,notificationEmail,phone,isUnlimited)
    def get_users(self,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"All",page=page,perPage=perPage)
    def get_user_by_id(self,idUser,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"IdUser",idUser,page=page,perPage=perPage)
    def get_user_by_email(self, email,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"Email",None,email,page=page,perPage=perPage)
    def get_user_by_tax_id(self, taxId,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"TaxId",None,None,taxId,page=page,perPage=perPage)
    def get_users_by_is_active(self, isActive,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"IsActive",None,None,None,isActive,page=page,perPage=perPage)
    def get_user_by_name(self, name,page=None,perPage=None):
        return AccountUserRequest.get_users(self.url_api,self.get_token(),"Name",name=name,page=page,perPage=perPage)
