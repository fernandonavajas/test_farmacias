from flask import Flask
import unittest 
from unittest import mock
from  pytest_mock import mocker
import responses

from api.farmacias import configure_routes


class TestFarmacias(unittest.TestCase):

    def test_base_route(self):
        app = Flask(__name__)
        configure_routes(app)
        client = app.test_client()
        url = '/'

        response = client.get(url)
        assert response.status_code == 200


    @responses.activate
    def test_buscador_succesfull(self):
        app = Flask(__name__)
        configure_routes(app)

        url_obtain_comunas = 'https://farmanet.minsal.cl/maps/index.php/ws/getLocalesRegion?id_region=7'
        responses.add(responses.POST, url_obtain_comunas, status=200)
        client = app.test_client()
        url = '/buscador'
        mock_request_form_data = {
            'comuna': '122',
            'nombre_local':'AHUMADA'
        }

        response = client.get(url,data= mock_request_form_data)
        assert 200 == response.status_code


    def test_ordenarResponse_succesfull(self):
        data = [
            {
                "fecha": "12-07-2020",
                "local_id": "910",
                "local_nombre": "MAESTRE",
                "comuna_nombre": "INDEPENDENCIA",
                "localidad_nombre": "INDEPENDENCIA",
                "local_direccion": "AV. SALOMON SACK 928",
                "funcionamiento_hora_apertura": "08:30 hrs.",
                "funcionamiento_hora_cierre": "21:30 hrs.",
                "local_telefono": "+560227376512",
                "local_lat": "-33.414275",
                "local_lng": "-70.678147",
                "funcionamiento_dia": "domingo",
                "fk_region": "7",
                "fk_comuna": "94"
            }
        ]
        self.assertIs(type(configure_routes.ordenarResponse(data)),str)
    
    def test_ordenarResponse_without_values(self):
        data = [{}]
        self.assertIs(type(configure_routes.ordenarResponse(data)),str)
