import unittest
import os
import sys
import uuid

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from AccountUser.AccountUser import AccountUser
from Balance.Balance import Balance

class TestBalance(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    urlApi = "https://api.test.sw.com.mx"
    comment = "Prueba unitaria Python"
    #Identificadores que el servicio rechaza, usados en las pruebas de error.
    invalidId = "no-es-uuid"
    notFoundId = "00000000-0000-0000-0000-000000000000"
    _childUserId = None

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
    def child_user_id(cls):
        #El idUser se toma de la propia cuenta distribuidora, nunca se hardcodea.
        if cls._childUserId is None:
            accountUser = AccountUser(cls.url, cls.urlApi, cls.token)
            response = accountUser.getUser_all()
            if response.get_status() != cls.expected or not response.data.items:
                raise unittest.SkipTest("La cuenta de pruebas no tiene cuentas hijas")
            cls._childUserId = response.data.items[0].idUser
        return cls._childUserId

    #UT Consulta del saldo propio
    def testBalance_auth(self):
        balance = Balance(self.url, self.urlApi, None, self.user, self.password)
        response = balance.get_balance()
        self.assertEqual(self.expected, response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertIsNotNone(response.data.idUser)
        self.assertIsNotNone(response.data.idUserBalance)
        self.assertIsNotNone(response.data.stampsAssigned)
        self.assertIsNotNone(response.data.stampsUsed)
        self.assertIsNotNone(response.data.stampsBalance)

    def testBalance(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.get_balance()
        self.assertEqual(self.expected, response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertIsNotNone(response.data.idUser)
        self.assertIsNotNone(response.data.idUserBalance)
        self.assertIsNotNone(response.data.stampsAssigned)
        self.assertIsNotNone(response.data.stampsUsed)
        self.assertIsNotNone(response.data.stampsBalance)

    #UT Consulta del saldo de una cuenta hija
    def testBalanceById_auth(self):
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, None, self.user, self.password)
        response = balance.get_balance_by_id(idUser)
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(idUser.lower(), response.data.idUser.lower())
        self.assertIsNotNone(response.data.stampsBalance)

    def testBalanceById(self):
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.get_balance_by_id(idUser)
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(idUser.lower(), response.data.idUser.lower())
        self.assertIsNotNone(response.data.idUserBalance)
        self.assertIsNotNone(response.data.stampsAssigned)
        self.assertIsNotNone(response.data.stampsUsed)
        self.assertIsNotNone(response.data.stampsBalance)

    def testBalanceById_uuid(self):
        #El idUser también se acepta como uuid.UUID, no sólo como cadena.
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.get_balance_by_id(uuid.UUID(idUser))
        self.assertEqual(self.expected, response.get_status())
        self.assertEqual(idUser.lower(), response.data.idUser.lower())

    def testBalanceById_invalidId(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.get_balance_by_id(self.invalidId)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testBalanceById_notFound(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.get_balance_by_id(self.notFoundId)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(404, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    #UT Asignación y remoción de timbres
    #El ciclo agrega y remueve la misma cantidad, de modo que el saldo queda como estaba.
    def testBalance_stamps_auth(self):
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, None, self.user, self.password)
        inicial = balance.get_balance_by_id(idUser).data.stampsBalance
        add = balance.add_stamps(idUser, 1, self.comment)
        self.assertEqual(self.expected, add.get_status())
        self.assertEqual(inicial + 1, add.get_data())
        try:
            consulta = balance.get_balance_by_id(idUser)
            self.assertEqual(inicial + 1, consulta.data.stampsBalance)
        finally:
            remove = balance.remove_stamps(idUser, 1, self.comment)
        self.assertEqual(self.expected, remove.get_status())
        self.assertEqual(inicial, remove.get_data())

    def testBalance_stamps(self):
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, self.token)
        inicial = balance.get_balance_by_id(idUser).data.stampsBalance
        add = balance.add_stamps(idUser, 1, self.comment)
        self.assertEqual(self.expected, add.get_status())
        self.assertEqual(inicial + 1, add.get_data())
        try:
            consulta = balance.get_balance_by_id(idUser)
            self.assertEqual(inicial + 1, consulta.data.stampsBalance)
        finally:
            remove = balance.remove_stamps(idUser, 1, self.comment)
        self.assertEqual(self.expected, remove.get_status())
        self.assertEqual(inicial, remove.get_data())

    def testBalance_stamps_uuid(self):
        idUser = uuid.UUID(self.child_user_id())
        balance = Balance(self.url, self.urlApi, self.token)
        add = balance.add_stamps(idUser, 1, self.comment)
        try:
            self.assertEqual(self.expected, add.get_status())
        finally:
            remove = balance.remove_stamps(idUser, 1, self.comment)
        self.assertEqual(self.expected, remove.get_status())
        self.assertEqual(add.get_data() - 1, remove.get_data())

    def testBalance_stamps_withoutComment(self):
        #El comentario es opcional para el servicio.
        idUser = self.child_user_id()
        balance = Balance(self.url, self.urlApi, self.token)
        add = balance.add_stamps(idUser, 1, None)
        try:
            self.assertEqual(self.expected, add.get_status())
        finally:
            remove = balance.remove_stamps(idUser, 1, "")
        self.assertEqual(self.expected, remove.get_status())
        self.assertEqual(add.get_data() - 1, remove.get_data())

    #UT de Error
    def testBalance_add_invalidId(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.add_stamps(self.invalidId, 1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testBalance_remove_invalidId(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.remove_stamps(self.invalidId, 1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testBalance_add_notFound(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.add_stamps(self.notFoundId, 1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testBalance_remove_notFound(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.remove_stamps(self.notFoundId, 1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testBalance_add_zeroStamps(self):
        #El servicio es quien valida que la cantidad sea mayor que cero.
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.add_stamps(self.child_user_id(), 0, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIn("Stamps", response.get_message())

    def testBalance_remove_negativeStamps(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.remove_stamps(self.child_user_id(), -1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIn("Stamps", response.get_message())

    def testBalance_remove_insufficientStamps(self):
        balance = Balance(self.url, self.urlApi, self.token)
        response = balance.remove_stamps(self.child_user_id(), 999999999, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(400, response.get_status_code())
        self.assertIn("saldo", response.get_message())

    def testBalance_invalidToken(self):
        balance = Balance(self.url, self.urlApi, "token-invalido")
        response = balance.add_stamps(self.child_user_id(), 1, self.comment)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertEqual(401, response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBalance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
