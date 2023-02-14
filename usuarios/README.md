# Microservicio Gestión de usuarios
El microservicio de gestión de usuarios permite crear usuarios y validar la identidad de un usuario por medio de tokens.

## API
1. **Creación de usuarios:** Crea un usuario con los datos brindados, el nombre del usuario debe ser único, así como el correo. POST ```/users```
2. **Generación de token:** Genera un nuevo Token para el usuario al que le corresponde el username y la contraseña. POST ```/users/auth```
3. **Consultar información del usuario:** Retorna los datos del usuario al que pertenece el token. GET ```/users/me```
4. **Consulta de salud del servicio:** Usado para verificar el estado de la aplicación. GET ```/users/ping```

## Ejecución con Docker
Se debe estar en la carpeta **usuarios**
1. Para ejecutar la aplicación con Docker compose: ```docker compose up -d```
2. Detener los contenedores de Docker compose: ```docker-compose stop```
3. Reiniciar los contenedores de Docker compose: ```docker-compose start```
4. La aplicación queda ejecutando en el puerto 3000 del localhost: ```http://localhost:3000```
5. Se configuró una base de datos PostgreSQL en el puerto 5433 por el localhost pero en el puerto 5432 dentro de Docker. Es posible acceder a los datos mediante programas como pgAdmin, configurando el puerto 5433 y los datos de la conexión

## Ejecución manual (En Linux - Ubuntu)
Se debe estar en la carpeta **usuarios**
1. Crear ambiente virtual: `python3 -m venv .venv`
2. Activar ambiente virtual: `source .venv/bin/activate`
3. Validar en la consola que se tiene activo el ambiente virtual, para desactivar env: `deactivate`
4. Instalar requirements: `python3 -m pip install -r requirements.txt`
5. Configurar base de datos SQLite: `export DATABASE_URL="sqlite:///usuarios.db"`
5. Cambiar el directorio: `cd src`
6. Ejecutar aplicación Flask: `flask run`
7. La aplicación queda ejecutando en el puerto 5000 del localhost: ```http://localhost:5000```

## Ejecución local de pruebas (En Linux - Ubuntu)
Se debe estar en la carpeta **usuarios** y haber ejecutado correctamente la aplicación en los pasos anteriores
1. Para ejecutar todas las pruebas: `python -m unittest discover -s tests -v`
2. Para ejecutar un conjunta de pruebas test_users.py: `python -m unittest tests/test_users.py`
3. Para conocer la cobertura de pruebas: `python -m coverage run -m unittest`
4. Para el reporte de pruebas en consola: `python -m coverage report`
5. Para el reporte detallado de las pruebas en archivo html: `python -m coverage html`