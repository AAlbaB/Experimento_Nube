from src import create_app
from flask_restful import Api
from .models import db
from .views import VistaCrearTrayectos, VistaGetTrayecto, VistaGetTrayectos, VistaPong, ViewTrayectos
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCrearTrayectos, '/routes')
api.add_resource(VistaGetTrayectos, '/routes')
api.add_resource(VistaGetTrayecto, '/routes/<int:route_id>')
api.add_resource(VistaPong, '/routes/ping')
api.add_resource(ViewTrayectos, '/routes/all')

jwt = JWTManager(app)
