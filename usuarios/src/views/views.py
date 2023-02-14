import uuid
from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, decode_token
from ..models import db, User, UserSchema
from ..utils import encryptPassword

user_schema = UserSchema()


class ViewUsers(Resource):

    def get(self):
        # Retorna todos los usuarios registrados
        # Endpoint http://localhost:5000/users/all

        return [user_schema.dump(user) for user in User.query.all()]


class VistaSignUp(Resource):

    def post(self):
        # Crea un usuario en la aplicacion
        # Endpoint http://localhost:5000/users
        try:
            user_username = User.query.filter(
                User.username == request.json['username']).first()

            user_email = User.query.filter(
                User.email == request.json['email']).first()

            user_pass = request.json['password']

            if len(request.json['username'].strip()) == 0:
                return {'mensaje': 'El nombre de usuario no puede estar vacío'}, 400

            if len(request.json['email'].strip()) == 0:
                return {'mensaje': 'El correo electrónico no puede estar vacío'}, 400

            if len(request.json['password'].strip()) == 0:
                return {'mensaje': 'La contraseña puede estar vacía'}, 400

            if user_username is not None:
                return {'mensaje': 'Nombre de usuario ya existe, por favor iniciar sesión'}, 412

            if user_email is not None:
                return {'mensaje': 'Correo electronico ya existe, por favor iniciar sesión'}, 412

            salt = uuid.uuid4().hex
            password_hash = encryptPassword(salt, user_pass)

            new_user = User(username=request.json['username'],
                            email=request.json['email'],
                            password=password_hash,
                            salt=salt)

            db.session.add(new_user)
            db.session.commit()

            return {'id': new_user.id, 'createdAt': new_user.createdAt.isoformat(timespec='seconds')}, 201

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class VistaLogIn(Resource):

    def post(self):
        # Loguea un usuario en la aplicacion
        # Endpoint http://localhost:5000/users/auth

        try:
            usuario = User.query.filter(
                User.username == request.json['username']).first()

            if len(request.json['username'].strip()) == 0:
                return {'mensaje': 'El nombre de usuario no puede estar vacío'}, 400

            if len(request.json['password'].strip()) == 0:
                return {'mensaje': 'La contraseña puede estar vacía'}, 400

            if usuario is None:
                return {'mensaje': 'El usuario no existe'}, 404

            salt = usuario.salt
            user_pass = usuario.password
            input_pass = encryptPassword(salt, request.json['password'])

            if user_pass != input_pass:
                return {'mensaje': 'La contraseña es incorrecta'}, 404

            token_de_acceso = create_access_token(identity=usuario.id)
            expireAt = datetime.now() + timedelta(minutes=15)

            usuario.token = token_de_acceso
            usuario.expireAt = expireAt
            db.session.commit()

            return {'id': usuario.id, 'token': token_de_acceso, 'expireAt': expireAt.isoformat(timespec='seconds')}, 200

        except Exception as e:
            return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503


class VistaUser(Resource):

    def get(self):
        # Retorna un usuario por su id
        # Endpoint http://localhost:5000/users/me

        try:
            token = request.headers.get('Authorization', None)[7:]
            valid_data = decode_token(token, allow_expired=True)
            userId = valid_data['sub']
            usuario = User.query.filter(User.id == userId).first()

            processData = datetime.now().isoformat()

            tokenDate = datetime.fromtimestamp(
                int(valid_data['exp'])).isoformat()

            tokenBD = usuario.token

            if processData > tokenDate:
                return {'mensaje': 'El token esta vencido'}, 401

            if tokenBD != token:
                return {'mensaje': 'El token no es valido'}, 401

            return user_schema.dump(usuario), 200

        except Exception as e:
            return {'mensaje': 'Por favor ingresar un token válido'}, 400


class VistaPong(Resource):

    def get(self):
        # Retorna pong
        # Endpoint http://localhost:5000/users/ping
        return 'pong', 200
