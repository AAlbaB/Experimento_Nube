from src import create_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .models import db
from .views import ViewUsers, VistaSignUp, VistaLogIn, VistaUser, VistaPong

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(ViewUsers, '/users/all')
api.add_resource(VistaSignUp, '/users')
api.add_resource(VistaLogIn, '/users/auth')
api.add_resource(VistaUser, '/users/me')
api.add_resource(VistaPong, '/users/ping')

jwt = JWTManager(app)
