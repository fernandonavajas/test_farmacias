from flask import Flask
import unittest , json
from unittest import mock
from  pytest_mock import mocker
import responses

from api.farmacias import configure_routes

url_obtain_farmacias = 'https://farmanet.minsal.cl/maps/index.php/ws/getLocalesRegion'


class TestFarmacias(unittest.TestCase):


    def test_base_route(self):
        app = Flask(__name__)
        configure_routes(app)
        client = app.test_client()
        url = '/'

        response = client.get(url)
        assert response.status_code == 200

    
    @responses.activate
    def test_farmacia_succesfull(self):
        app = Flask(__name__)
        configure_routes(app)
        body = '''[
            {
            "fecha": "13-07-2020",
            "local_id": "534",
            "local_nombre": "TORRES MPD",
            "comuna_nombre": "RECOLETA",
            "localidad_nombre": "RECOLETA",
            "local_direccion": "AVENIDA EL SALTO 2972",
            "funcionamiento_hora_apertura": "10:30 hrs.",
            "funcionamiento_hora_cierre": "19:30 hrs.",
            "local_telefono": "+560225053570",
            "local_lat": "-33.3996351",
            "local_lng": "-70.62894990000001",
            "funcionamiento_dia": "lunes",
            "fk_region": "7",
            "fk_comuna": "122"
            }
        ]'''
        
        responses.add(responses.GET,url_obtain_farmacias,body=body, status=200)
        client = app.test_client()
        url = '/buscador'
        mock_request_form_data = {
            'comuna': '122',
            'nombre_local':'TORRES MPD'
        }

        response = client.get(url,data= mock_request_form_data)
        assert 200 == response.status_code


    @responses.activate
    def test_farmacia_no_encontrada(self):
        app = Flask(__name__)
        configure_routes(app)

        body = '''[
            {
                "fecha": "12-07-2020"
            }
        ]'''

        responses.add(responses.GET, url_obtain_farmacias,body=body, status=200)
        client = app.test_client()
        url = '/buscador'
        mock_request_form_data = {
            'comuna': '999',
            'nombre_local':'Farmacia Fuentes'
        }
        response = client.get(url,data= mock_request_form_data)
        
        assert 200 == response.status_code


    @responses.activate
    def test_farmacia_error_obtener_locales(self):
        app = Flask(__name__)
        configure_routes(app)

        responses.add(responses.GET, url_obtain_farmacias, status=500)
        client = app.test_client()
        url = '/buscador'
        mock_request_form_data = {
            'comuna': '122',
            'nombre_local':'AHUMADA'
        }

        response = client.get(url,data= mock_request_form_data)
        assert 500 == response.status_code
    

        
