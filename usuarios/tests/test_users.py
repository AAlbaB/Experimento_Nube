import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from src.app import app
from src.models import User, db


class TestUsuario(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.user_pass = self.data_factory.password()
        self.user_username = self.data_factory.name()
        self.user_email = self.data_factory.email()

        newUser = {
            "username": self.user_username,
            "email": self.user_email,
            "password": self.user_pass
        }

        sol_newUser = self.client.post("/users",
                                       data=json.dumps(newUser),
                                       headers={'Content-Type': 'application/json'})

        respuestaUser = json.loads(sol_newUser.get_data())

        self.user_id = respuestaUser["id"]
        self.user_createdAt = respuestaUser["createdAt"]

    def tearDown(self):

        usuarios = User.query.all()
        for usuario in usuarios:
            db.session.delete(usuario)

        db.session.commit()

    def test_obtener_usuarios(self):

        newUser = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": self.data_factory.password()
        }

        headers = {'Content-Type': 'application/json'}

        users_before = self.client.get("/users/all", headers=headers)
        len_users_before = len(json.loads(users_before.get_data()))

        sol_newUser = self.client.post("/users",
                                       data=json.dumps(newUser),
                                       headers={'Content-Type': 'application/json'})

        users_after = self.client.get("/users/all", headers=headers)
        len_users_after = len(json.loads(users_after.get_data()))

        self.assertEqual(len_users_before, 1)
        self.assertEqual(sol_newUser.status_code, 201)
        self.assertEqual(len_users_after, 2)

    def test_crear_usuario(self):

        newUser = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": self.data_factory.password()
        }

        endpoint_usuario = "/users"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 201)

    def test_crear_usuario_error(self):

        newUser = {
            "username": 1234567,
            "email": self.data_factory.email(),
            "password": self.data_factory.password()
        }

        endpoint_usuario = "/users"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 503)

    def test_crear_usuario_faltante(self):

        newUser = {
            "username": '',
            "email": self.data_factory.email(),
            "password": self.data_factory.password()
        }

        newUserTwo = {
            "username": self.data_factory.name(),
            "email": '',
            "password": self.data_factory.password()
        }

        newUserThree = {
            "username": self.data_factory.name(),
            "email": self.data_factory.email(),
            "password": ''
        }

        endpoint_usuario = "/users"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(newUser),
                                       headers=headers)

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(newUserTwo),
                                           headers=headers)

        sol_newUser_Three = self.client.post(endpoint_usuario,
                                             data=json.dumps(newUserThree),
                                             headers=headers)

        self.assertEqual(sol_newUser.status_code, 400)
        self.assertEqual(sol_newUser_Two.status_code, 400)
        self.assertEqual(sol_newUser_Three.status_code, 400)

    def test_crear_usuario_existente(self):

        newUserTwo = {
            "username": self.user_username,
            "email": self.data_factory.email(),
            "password": self.data_factory.password()
        }

        newUserThree = {
            "username": self.data_factory.name(),
            "email": self.user_email,
            "password": self.data_factory.password()
        }

        endpoint_usuario = "/users"
        headers = {'Content-Type': 'application/json'}

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(newUserTwo),
                                           headers=headers)

        sol_newUser_Three = self.client.post(endpoint_usuario,
                                             data=json.dumps(newUserThree),
                                             headers=headers)

        self.assertEqual(sol_newUser_Two.status_code, 412)
        self.assertEqual(sol_newUser_Three.status_code, 412)

    def test_login_exitoso(self):

        loginUser = {
            "username": self.user_username,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/auth"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 200)

    def test_login_faltante(self):

        loginUser = {
            "username": '',
            "password": self.user_pass
        }

        loginUserTwo = {
            "username": self.user_username,
            "password": ''
        }

        endpoint_usuario = "/users/auth"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(loginUserTwo),
                                           headers=headers)

        self.assertEqual(sol_newUser.status_code, 400)
        self.assertEqual(sol_newUser_Two.status_code, 400)

    def test_login_fallido(self):

        loginUser = {
            "username": self.data_factory.name(),
            "password": self.user_pass
        }

        loginUserTwo = {
            "username": self.user_username,
            "password": self.data_factory.password()
        }

        endpoint_usuario = "/users/auth"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        sol_newUser_Two = self.client.post(endpoint_usuario,
                                           data=json.dumps(loginUserTwo),
                                           headers=headers)

        self.assertEqual(sol_newUser.status_code, 404)
        self.assertEqual(sol_newUser_Two.status_code, 404)

    def test_login_error(self):

        loginUser = {
            "username": 123456,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/auth"
        headers = {'Content-Type': 'application/json'}

        sol_newUser = self.client.post(endpoint_usuario,
                                       data=json.dumps(loginUser),
                                       headers=headers)

        self.assertEqual(sol_newUser.status_code, 503)

    def test_user_exitoso(self):

        loginUser = {
            "username": self.user_username,
            "password": self.user_pass
        }

        endpoint_usuario = "/users/auth"
        headers = {'Content-Type': 'application/json'}

        sol_login = self.client.post(endpoint_usuario,
                                     data=json.dumps(loginUser),
                                     headers=headers)

        respuestaUser = json.loads(sol_login.get_data())
        token = respuestaUser["token"]

        endpoint_me = "/users/me"
        headers_token = {'Content-Type': 'application/json',
                         "Authorization": "Bearer {}".format(token)}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_token)

        self.assertEqual(sol_login.status_code, 200)
        self.assertEqual(sol_me.status_code, 200)

    def test_user_fallido(self):
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6' + \
                'ZmFsc2UsImlhdCI6MTY3NTgyMTY4NSwianRpIjoiOGEyY2JiNTA' + \
                'tNDAyYi00OTM5LWIwYmUtODU2M2RhMWEyODdjIiwidHlwZSI6ImF' + \
                'jY2VzcyIsInN1YiI6MSwibmJmIjoxNjc1ODIxNjg1LCJleHAiOjE' + \
                '2NzU4MjI1ODV9.KbV7iOfk6xhd_9C-j7nVyjrLoP-_MyJdKP87b708_kE'

        endpoint_me = "/users/me"
        headers_me = {'Content-Type': 'application/json',
                      "Authorization": "Bearer {}".format(token)}

        sol_autho = self.client.get(endpoint_me,
                                    headers=headers_me)

        self.assertEqual(sol_autho.status_code, 401)

    def test_user_error(self):
        token = ''

        endpoint_me = "/users/me"
        headers_token = {'Content-Type': 'application/json',
                         "Authorization": "Bearer {}".format(token)}

        sol_me = self.client.get(endpoint_me,
                                 headers=headers_token)

        self.assertEqual(sol_me.status_code, 400)

    def test_ping_users(self):

        endpoint_ping = "/users/ping"
        headers = {'Content-Type': 'application/json'}

        sol_ping = self.client.get(endpoint_ping,
                                   headers=headers)

        self.assertEqual(sol_ping.status_code, 200)
