from flask import Flask
from flask import request
import requests, json

def configure_routes(app):
    @app.route('/')
    def home():

        url_obtain_comunas = 'https://midastest.minsal.cl/farmacias/maps/index.php/utilidades/maps_obtener_comunas_por_regiones'
        request_obtain_comunas = {
            'reg_id': 7
        }
        response_invoice = requests.post(url_obtain_comunas,request_obtain_comunas)
        if response_invoice.status_code not in [200]:
            return {"status":"Error",
                    "message": "Error del servicio midastest.minsal.cl/farmacias",
                    "codigo": response_invoice.status_code }, 500

        return template_home(response_invoice.text)


    @app.route('/buscador', methods = ['GET'])
    def buscadorDeFarmacias():
        # 1. Obtener y validar input
        comuna = request.args.get('comuna','').upper()
        nombre_local = request.args.get('nombre_local','').upper()
        region = 7 # Region Metropolitana

        # 2. Obtener farmacias
        url_list_farmacias = 'https://farmanet.minsal.cl/maps/index.php/ws/getLocalesRegion?id_region='+str(region)
        response_farmacias = requests.get(url_list_farmacias)
        if response_farmacias.status_code not in [200]:
            return {"status":"Error del servicio farmanet.minsal.cl/getLocalesRegion",
                    "codigo": response_invoice.status_code }

        #3. Filtrar farmacias por comuna y/o nombre
        if not response_farmacias.text:
            return {"status":"Error",
                    "message": "El servicio midastest.minsal.cl/farmacias respondio vacio" }, 412 
        input_dict = json.loads(response_farmacias.text)

        # Filtro por comuna
        if comuna:
            input_dict = [x for x in input_dict if x.get('fk_comuna') == comuna]

        # Filtro solo por nombre del local
        if nombre_local:
            input_dict = [x for x in input_dict if x.get('local_nombre').strip() == nombre_local]

        # 4. Armar el response según lo solicitado
        return ordenarResponse(input_dict), 200, {"Content-Type":"application/json"}


    def ordenarResponse(input_dict):
        response=[]

        for x in input_dict:
            specific_values_dict = {}
            specific_values_dict['Nombre del local'] = x.get('local_nombre','') or ''
            specific_values_dict['Dirección'] = x.get('local_direccion','') or ''
            specific_values_dict['Teléfono'] = x.get('local_telefono','') or ''
            specific_values_dict['Latitud'] = x.get('local_lat','') or ''
            specific_values_dict['Longitud'] = x.get('local_lng','') or ''
            response.append(specific_values_dict)

        return json.dumps(response)


    def template_home(opciones):
        return ('''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Test Consorcio</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            </head>

            <body style='background-color:aliceblue;text-align: center;'>
                <h1 style='color: orange;'>Busca tus farmacias por sector</h1>
                <div style='display: row'>
                    <label for="cars">Elije una comuna </label>
                    <select name="comunas">
                    '''+opciones+'''
                    </select>
                    <br><br>
                    <label for="local">Nombre del Local</label>
                    <input type="text" id="local" name="local" placeholder="Ex: Cruz verde">
                    <br><br>
                    <input type = "button" onclick = "myfunc()" value = "Buscar">
                </div>
            </body>
            </html>
            <script>
                function myfunc()
                {
                    var comuna_elegida = document.getElementsByName('comunas')[0];
                    var index = comuna_elegida.selectedIndex
                    glosa_comuna = comuna_elegida.options[index].text
                    codigo_comuna = comuna_elegida.options[index].value

                    var nombre_del_local = document.getElementsByName('local')[0];
                    console.log(nombre_del_local.value)
                    url_redirect = "http://127.0.0.1:5000/buscador?comuna="+codigo_comuna+"&nombre_local="+nombre_del_local.value
                    
                    window.location.href = url_redirect;
                }
                
            </script>
        ''')
