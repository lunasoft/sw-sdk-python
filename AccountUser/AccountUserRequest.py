from urllib.parse import urlencode
from AccountUser.AccountUserResponse import AccountUserResponse
from Utils.requestHelper import RequestHelper

class AccountUserRequest():
    _pathBase = "/management/v2/api/dealers/users"
    @staticmethod
    def get_path(filter,idUser,email,taxId, isActive, name=None, page=None, perPage=None):
        """Arma la ruta de consulta con el filtro solicitado y la paginación."""
        parameters = {}
        if filter == "IdUser":
            parameters["IdUser"] = idUser
        elif filter == "Email":
            parameters["Email"] = email
        elif filter == "TaxId":
            parameters["TaxId"] = taxId
        elif filter == "IsActive":
            parameters["IsActive"] = isActive
        elif filter == "Name":
            parameters["Name"] = name
        if page is not None:
            parameters["Page"] = page
        if perPage is not None:
            parameters["PerPage"] = perPage
        path = AccountUserRequest._pathBase
        if parameters:
            path = path + "?" + urlencode(parameters)
        return path

    @staticmethod
    def get_users(urlApi,token,filter,idUser=None,email=None,taxId=None, isActive=None, name=None, page=None, perPage=None):
        """Consulta los usuarios asociados al token, con el filtro y la página indicados."""
        path = AccountUserRequest.get_path(filter,idUser,email,taxId, isActive, name, page, perPage)
        endpoint = urlApi + path
        response = RequestHelper.get_json_request(endpoint,token)
        return AccountUserResponse(response)

    @staticmethod
    def create_user(urlApi,token,name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone):
        """Da de alta un usuario en la cuenta distribuidora."""
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
        """Elimina un usuario de la cuenta distribuidora."""
        endpoint = urlApi + AccountUserRequest._pathBase + f"/{idUser}"
        response = RequestHelper.delete_json_request(endpoint,token)
        return AccountUserResponse(response)

    @staticmethod
    def update_user(urlApi,token,idUser,name,taxId,notificationEmail,phone,isUnlimited):
        """Actualiza los datos de un usuario previamente registrado."""
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
