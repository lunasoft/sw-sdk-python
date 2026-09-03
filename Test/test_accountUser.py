import unittest
import os
import random
import string
import sys
from datetime import datetime

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from AccountUser.AccountUser import AccountUser

class TestAccountUser(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    taxId = "XAXX010101000"
    phone = "0000000000"
    notFoundId = "00000000-0000-0000-0000-000000000000"
    invalidId = "no-es-uuid"
    _firstUser = None

    #Las credenciales de la cuenta de pruebas nunca van en el código.
    user = os.environ.get("SDKTEST_USER")
    password = os.environ.get("SDKTEST_PASSWORD")
    token = os.environ.get("SDKTEST_TOKEN")

    @classmethod
    def setUpClass(cls):
        for nombre, valor in (("SDKTEST_USER", cls.user),
                              ("SDKTEST_PASSWORD", cls.password),
                              ("SDKTEST_TOKEN", cls.token)):
            if not valor:
                raise ValueError(f"Falta la variable de entorno {nombre}")

    @classmethod
    def first_user(cls):
        #Los datos de consulta se toman de la propia cuenta, nunca se hardcodean.
        if cls._firstUser is None:
            accountUser = AccountUser(cls.url, cls.urlApi, cls.token)
            response = accountUser.getUser_all()
            if response.get_status() != cls.expected or not response.data.items:
                raise unittest.SkipTest("La cuenta de pruebas no tiene cuentas hijas")
            cls._firstUser = response.data.items[0]
        return cls._firstUser

    @staticmethod
    def generate_email():
        letters = ''.join(random.choices(string.ascii_lowercase, k=4))
        timestamp = datetime.now().strftime("%d%H%M%S")
        return f"ut.python.{letters}{timestamp}@example.com"

    @staticmethod
    def generate_password():
        #La contraseña se genera cumpliendo la política del servicio, nunca se escribe en el código.
        upper = ''.join(random.choices(string.ascii_uppercase, k=3))
        lower = ''.join(random.choices(string.ascii_lowercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"{upper}{lower}{numbers}$"

    #UT Auth consulta de usuarios
    def testAccountUser_all_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_all()
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_idUser_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_by_idUser(self.first_user().idUser)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_email_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_by_email(self.first_user().email)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_taxId_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_by_taxId(self.first_user().taxId)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_isActive_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_by_isActive(True)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_name_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        response = accountUser.getUser_by_name(self.first_user().name)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    #UT Token consulta de usuarios
    def testAccountUser_all(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_all()
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)
        for user in response.data.items:
            self.assertIsNotNone(user.idUser)
            self.assertIsNotNone(user.name)
            self.assertIsNotNone(user.email)

    def testAccountUser_by_idUser(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        idUser = self.first_user().idUser
        response = accountUser.getUser_by_idUser(idUser)
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(1, len(response.data.items))
        self.assertEqual(idUser.lower(), response.data.items[0].idUser.lower())

    def testAccountUser_by_email(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_email(self.first_user().email)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_taxId(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_taxId(self.first_user().taxId)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_isActive(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_isActive(True)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    def testAccountUser_by_name(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_name(self.first_user().name)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) > 0)

    #UT Paginación de la consulta
    def testAccountUser_pagination(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_all(1, 1)
        self.assertEqual(self.expected, response.get_status())
        self.assertTrue(len(response.data.items) <= 1)
        self.assertEqual(1, response.get_meta()["page"])
        self.assertEqual(1, response.get_meta()["perPage"])
        self.assertIsNotNone(response.get_links())

    def testAccountUser_pagination_emptyPage(self):
        #Una página sin resultados responde success con la lista vacía, no es un error.
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_all(999)
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(0, len(response.data.items))
        self.assertEqual(999, response.get_meta()["page"])

    def testAccountUser_pagination_invalidPerPage(self):
        #El servicio es quien limita el tamaño de página.
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_all(1, 100)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    #UT Alta, actualización y baja de usuarios, destructivas: dan de alta una cuenta real en el
    #distribuidor y la eliminan en la misma prueba, de modo que la cuenta queda como estaba.
    #Para ejecutarlas basta con definir SDKTEST_USER_LIFECYCLE.
    @unittest.skipUnless(os.environ.get("SDKTEST_USER_LIFECYCLE"), "Prueba destructiva, definir SDKTEST_USER_LIFECYCLE para ejecutarla")
    def testAccountUser_lifecycle(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        email = self.generate_email()
        alta = accountUser.create_user("Prueba UT Python", self.taxId, email, 0, False,
                                       self.generate_password(), email, self.phone)
        self.assertEqual(self.expected, alta.get_status())
        #El alta regresa el usuario creado, la actualización y la baja regresan su idUser.
        idUser = alta.data.idUser
        self.assertIsNotNone(idUser)
        self.addCleanup(accountUser.delete_user, idUser)

        consulta = accountUser.getUser_by_email(email)
        self.assertEqual(self.expected, consulta.get_status())
        self.assertEqual(1, len(consulta.data.items))
        self.assertEqual(idUser.lower(), consulta.data.items[0].idUser.lower())

        actualizacion = accountUser.update_user(idUser, "Prueba UT Python Editado", self.taxId, email, "0000000001")
        self.assertEqual(self.expected, actualizacion.get_status())
        self.assertEqual(idUser, actualizacion.get_data())

        baja = accountUser.delete_user(idUser)
        self.assertEqual(self.expected, baja.get_status())
        self.assertIsNotNone(baja.get_data())
        self.assertEqual(0, len(accountUser.getUser_by_email(email).data.items))

    @unittest.skipUnless(os.environ.get("SDKTEST_USER_LIFECYCLE"), "Prueba destructiva, definir SDKTEST_USER_LIFECYCLE para ejecutarla")
    def testAccountUser_lifecycle_auth(self):
        accountUser = AccountUser(self.url, self.urlApi, None, self.user, self.password)
        email = self.generate_email()
        alta = accountUser.create_user("Prueba UT Python", self.taxId, email, 0, False,
                                       self.generate_password(), email, self.phone)
        self.assertEqual(self.expected, alta.get_status())
        idUser = alta.data.idUser
        self.addCleanup(accountUser.delete_user, idUser)

        baja = accountUser.delete_user(idUser)
        self.assertEqual(self.expected, baja.get_status())
        self.assertIsNotNone(baja.get_data())

    @unittest.skipUnless(os.environ.get("SDKTEST_USER_LIFECYCLE"), "Prueba destructiva, definir SDKTEST_USER_LIFECYCLE para ejecutarla")
    def testAccountUser_update_sameData(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        email = self.generate_email()
        alta = accountUser.create_user("Prueba UT Python", self.taxId, email, 0, False,
                                       self.generate_password(), email, self.phone)
        self.assertEqual(self.expected, alta.get_status())
        idUser = alta.data.idUser
        self.addCleanup(accountUser.delete_user, idUser)
        response = accountUser.update_user(idUser, "Prueba UT Python", self.taxId, email, self.phone)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    #UT Consultas sin coincidencias
    def testAccountUser_by_idUser_notFound(self):
        #Una consulta sin coincidencias responde success con la lista vacía, no es un error.
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_idUser(self.notFoundId)
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(0, len(response.data.items))

    def testAccountUser_by_email_notFound(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_email("sin.coincidencias@example.com")
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(0, len(response.data.items))

    def testAccountUser_by_taxId_notFound(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_taxId("AAAA000101011")
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(0, len(response.data.items))

    #UT de Error
    def testAccountUser_by_idUser_invalid(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.getUser_by_idUser(self.invalidId)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testAccountUser_create_duplicatedEmail(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        email = self.first_user().email
        response = accountUser.create_user("Prueba UT Python", self.taxId, email, 0, False,
                                           self.generate_password(), email, self.phone)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testAccountUser_create_invalidPassword(self):
        #El servicio es quien valida la política de la contraseña.
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        email = self.generate_email()
        response = accountUser.create_user("Prueba UT Python", self.taxId, email, 0, False,
                                           "1234", email, self.phone)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testAccountUser_delete_notFound(self):
        accountUser = AccountUser(self.url, self.urlApi, self.token)
        response = accountUser.delete_user(self.notFoundId)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(404, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testAccountUser_invalidToken(self):
        accountUser = AccountUser(self.url, self.urlApi, "token-invalido")
        response = accountUser.getUser_all()
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(401, response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountUser)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
