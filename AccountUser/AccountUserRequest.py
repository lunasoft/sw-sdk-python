from AccountUser.AccountUserResponse import AccountUserResponse
from Utils.requestHelper import RequestHelper

class AccountUserRequest():
    _pathBase = "/management/v2/api/dealers/users"
    @staticmethod
    def get_path(filter,idUser,email,taxId, isActive):
        endpoint = AccountUserRequest._pathBase
        if filter == "All":
            path = endpoint
        elif filter == "IdUser":
            path = endpoint + "/?IdUser=" + idUser
        elif filter == "Email":
            path = endpoint + "/?Email=" + email
        elif filter == "TaxId":
            path = endpoint + "/?TaxId=" + taxId
        elif filter == "IsActive":
            path = endpoint + "/?IsActive=" + str(isActive)
        return path
    
    @staticmethod
    def get_users(urlApi,token,filter,idUser=None,email=None,taxId=None, isActive=None):
        path = AccountUserRequest.get_path(filter,idUser,email,taxId, isActive)
        endpoint = urlApi + path
        response = RequestHelper.get_json_request(endpoint,token)
        return AccountUserResponse(response)
    
    @staticmethod
    def create_user(urlApi,token,name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone):
        endpoint = urlApi + AccountUserRequest._pathBase
        payload = {
            "name": name,
            "taxId":taxId,
            "email":email,
            "stamps": stamps,
            "isUnlimited": isUnlimited,
            "password": password,
            "notificationEmail": notificationEmail,
            "phone":phone
        }
        response = RequestHelper.post_json_request(endpoint, token,payload)
        return AccountUserResponse(response)
    
    @staticmethod
    def delete_user(urlApi,token,idUser):
        endpoint = urlApi + AccountUserRequest._pathBase + f"/{idUser}"
        response = RequestHelper.delete_json_request(endpoint,token)
        return AccountUserResponse(response)
    
    @staticmethod
    def update_user(urlApi,token,idUser,name,taxId,notificationEmail,phone,isUnlimited):
        endpoint = urlApi + AccountUserRequest._pathBase + f"/{idUser}"
        payload = {
            "idUser": idUser,
            "name": name,
            "taxId":taxId,
            "notificationEmail": notificationEmail,
            "phone":phone,
            "isUnlimited": isUnlimited
        }
        response = RequestHelper.put_json_request(endpoint,token,payload)
        return AccountUserResponse(response)