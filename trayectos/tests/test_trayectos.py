import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from src.app import app
from src.models import Trayecto, db
from unittest.mock import patch
from unittest import mock


class TestTrayecto(TestCase):

    @mock.patch("requests.get")
    def setUp(self, mock_get):

        self.data_factory = Faker()
        self.client = app.test_client()
        self.sourceAirportCode = 'ABC'
        self.destinyAirportCode = 'AGT'

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        newTrayecto = {
            "sourceAirportCode": self.sourceAirportCode,
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": self.destinyAirportCode,
            "destinyCountry": self.data_factory.city(),
            "bagCost": '250000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        respuestaTrayecto = json.loads(response.get_data())

        self.route_id = respuestaTrayecto["id"]
        self.route_createdAt = respuestaTrayecto["createdAt"]
        self.expireAt = respuestaTrayecto["expireAt"]

    def tearDown(self):

        trayectos = Trayecto.query.all()
        for trayecto in trayectos:
            db.session.delete(trayecto)

        db.session.commit()

    @mock.patch("requests.get")
    def test_crea_trayecto_exitoso(self, mock_get):

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        newTrayecto = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": 'CLO',
            "destinyCountry": self.data_factory.city(),
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        self.assertEqual(response.status_code, 201)

    @mock.patch("requests.get")
    def test_crear_trayecto_info_vacia(self, mock_get):

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        newTrayecto = {
            "sourceAirportCode": '',
            "sourceCountry": 'Bogota',
            "destinyAirportCode": 'LMN',
            "destinyCountry": 'Cali',
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        newTrayecto_dos = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": '',
            "destinyAirportCode": 'LMN',
            "destinyCountry": 'Cali',
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response_dos = app.test_client().post("/routes",
                                              data=json.dumps(newTrayecto_dos),
                                              headers={'Content-Type': 'application/json',
                                                       "Authorization": "Bearer {}".format(token)
                                                       })

        newTrayecto_tres = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": 'Bogota',
            "destinyAirportCode": '',
            "destinyCountry": 'Cali',
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response_tres = app.test_client().post("/routes",
                                               data=json.dumps(
                                                   newTrayecto_tres),
                                               headers={'Content-Type': 'application/json',
                                                        "Authorization": "Bearer {}".format(token)
                                                        })

        newTrayecto_cuatro = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": 'Bogota',
            "destinyAirportCode": 'CLO',
            "destinyCountry": '',
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response_cuatro = app.test_client().post("/routes",
                                                 data=json.dumps(
                                                     newTrayecto_cuatro),
                                                 headers={'Content-Type': 'application/json',
                                                          "Authorization": "Bearer {}".format(token)
                                                          })

        newTrayecto_cinco = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": 'Bogota',
            "destinyAirportCode": 'CLO',
            "destinyCountry": 'Cali',
            "bagCost": ''
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response_cinco = app.test_client().post("/routes",
                                                data=json.dumps(
                                                    newTrayecto_cinco),
                                                headers={'Content-Type': 'application/json',
                                                         "Authorization": "Bearer {}".format(token)
                                                         })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_dos.status_code, 400)
        self.assertEqual(response_tres.status_code, 400)
        self.assertEqual(response_cuatro.status_code, 400)
        self.assertEqual(response_cinco.status_code, 400)

    @mock.patch("requests.get")
    def test_crea_trayectoso_aeropuerto_nulo(self, mock_get):

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        newTrayecto = {
            "sourceAirportCode": 'XXX',
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": 'CLO',
            "destinyCountry": self.data_factory.city(),
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        newTrayecto_dos = {
            "sourceAirportCode": 'BOG',
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": 'XXX',
            "destinyCountry": self.data_factory.city(),
            "bagCost": '100000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response_dos = app.test_client().post("/routes",
                                              data=json.dumps(newTrayecto_dos),
                                              headers={'Content-Type': 'application/json',
                                                       "Authorization": "Bearer {}".format(token)
                                                       })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_dos.status_code, 400)

    @mock.patch("requests.get")
    def test_crea_trayecto_existente(self, mock_get):

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        newTrayecto = {
            "sourceAirportCode": 'ABC',
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": 'AGT',
            "destinyCountry": self.data_factory.city(),
            "bagCost": '250000'
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        self.assertEqual(response.status_code, 412)

    def test_crea_trayecto_sinToken(self):

        newTrayecto = {
            "sourceAirportCode": 'ABC',
            "sourceCountry": self.data_factory.city(),
            "destinyAirportCode": 'AGT',
            "destinyCountry": self.data_factory.city(),
            "bagCost": '250000'
        }

        token = "mitoken"

        response = app.test_client().post("/routes",
                                          data=json.dumps(newTrayecto),
                                          headers={'Content-Type': 'application/json',
                                                   "Authorization": "Bearer {}".format(token)
                                                   })

        self.assertEqual(response.status_code, 401)

    @mock.patch("requests.get")
    def test_consultar_trayectos_exitoso(self, mock_get):

        expected = {
            "id": 1,
            "username": "AndresTapia",
            "email": "andres@mail.com"
        }

        token = "mitoken"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected

        end_point = "routes?from={0}&to={1}&when={2}".format(
            self.sourceAirportCode, self.destinyAirportCode, '12/02/2023')
        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(token)}

        response = app.test_client().get(end_point, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_consultar_trayectos_sinToken(self):

        token = "mitoken"

        end_point = "routes?from={0}&to={1}&when={2}".format(
            self.sourceAirportCode, self.destinyAirportCode, '12/02/2023')
        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(token)}

        response = app.test_client().get(end_point, headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_ping_trayectos(self):

        endpoint_ping = "/routes/ping"
        headers = {'Content-Type': 'application/json'}

        sol_ping = self.client.get(endpoint_ping,
                                   headers=headers)

        self.assertEqual(sol_ping.status_code, 200)
