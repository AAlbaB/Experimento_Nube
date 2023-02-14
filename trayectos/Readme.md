# Microservicio Gestión de trayectos
El microservicio de gestión de trayectos permite crear trayectos y consultar los trayectos creados.

## API
1. **Creación de trayectos:** Crea un trayecto con los datos brindados, el token de usuario no debe estar vencido, tods los campos deben estar presentes en la solicitud, el trayecto no debe existir y estar activo. POST ```/routes```
2. **Buscar trayectos:** Busca los trayectos según los campos FROM, TO y WHEN, los campos son opcionales y en el caso de que ninguno esté presente se devolverá la lista de datos sin filtrar. El token no debe estar vencido, los tipos de datos ingresados deben ser correctos. GET ```/routes?from=code&to=code&when=start-date```
3. **Consultar trayecto:** Retorna un trayecto, solo un usuario autorizado puede realizar esta operación. GET ```/routes/{id}```
4. **Consulta de salud del servicio:** Usado para verificar el estado de la aplicación. GET ```/users/ping```

## Ejecución con Docker
Se debe estar en la carpeta **trayectos**
1. Para ejecutar la aplicación con Docker compose: ```docker compose up -d```
2. Detener los contenedores de Docker compose: ```docker-compose stop```
3. Reiniciar los contenedores de Docker compose: ```docker-compose start```
4. La aplicación queda ejecutando en el puerto 3002 del localhost: ```http://localhost:3002```
5. Se configuró una base de datos PostgreSQL en el puerto 5435 por el localhost pero en el puerto 5432 dentro de Docker. Es posible acceder a los datos mediante programas como pgAdmin, configurando el puerto 5435 y los datos de la conexión

## Ejecución manual (En Linux - Ubuntu)
Se debe estar en la carpeta **trayectos**
1. Crear ambiente virtual: `python3 -m venv .venv`
2. Activar ambiente virtual: `source .venv/bin/activate`
3. Validar en la consola que se tiene activo el ambiente virtual, para desactivar env: `deactivate`
4. Instalar requirements: `python3 -m pip install -r requirements.txt`
5. Configurar base de datos SQLite: `export DATABASE_URL="sqlite:///trayectos.db"`
5. Cambiar el directorio: `cd src`
6. Ejecutar aplicación Flask: `flask run`
7. La aplicación queda ejecutando en el puerto 5000 del localhost: ```http://localhost:5000```

## Ejecución local de pruebas (En Linux - Ubuntu)
Se debe estar en la carpeta **trayectos** y haber ejecutado correctamente la aplicación en los pasos anteriores
1. Para ejecutar todas las pruebas: `python -m unittest discover -s tests -v`
2. Para ejecutar un conjunta de pruebas test_users.py: `python -m unittest tests/test_trayectos.py`
3. Para conocer la cobertura de pruebas: `python -m coverage run -m unittest` en caso de que no funcione esta, sebe ejecutar: `coverage run -m unittest tests/test_trayectos.py -v`
4. Para el reporte de pruebas en consola: `python -m coverage report`
5. Para el reporte detallado de las pruebas en archivo html: `python -m coverage html`