## 1. Levantar el servicio en local

### Crear virtual enviroment  
python -m venv env  

### Activar enviroment 
source env/bin/activate

### Instalar librerias  
pip install -r requirements.txt  

### Iniciar proyecto
python app.py

## 2. Probar servicio
http://127.0.0.1:5000/
or
http://127.0.0.1:5000/buscador?comuna=83&nombre_local=cruz%20verde

## 3. Ejecutar pruebas unitarias

### Ejecutar pytest
python -m pytest

### Ejecutar test coverage
python -m pytest --cov="project"