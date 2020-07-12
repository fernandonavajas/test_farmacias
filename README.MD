# 1. Levantar el servicio en local:

## Crear virtual enviroment  
python3 -m venv env  

## Activar enviroment 
source env/bin/activate

## Instalar librerias  
pip install -r requirements.txt  

## Iniciar proyecto
cd project/api
python farmacias.py

# 2. Ejecutar pruebas unitarias

## Ejecutar pytest
python -m pytest

## Ejecutar test coverage
python -m pytest --cov="project"