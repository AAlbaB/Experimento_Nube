import json
from flask_restful import Resource
from flask import request
from datetime import datetime
from datetime import timedelta
from ..models import db, Trayecto, TrayectoSchemaList
import requests
from flask_jwt_extended import decode_token

trayecto_schema_list = TrayectoSchemaList()


AEROPUERTOS = [ 'ABC','AEP','AFA','AGP','AGT','AMS','ANF','AOL','ARI','ARN','ASU','ATH','AUA','BBA','BCN','BIN','BIO','BOD','BOG','BPM','BRC',
                'BSL','BST','BUD','BYJ','COR','CDT','CCC','CCP','CCS','CDG','CGN','CLO','CLX','CMN','CNQ','COC','CTC','CUE','CUU','CVU','CWB',
                'DAY','DJE','DME','DOH','DXB','EAP​','EDI','EGE','EIN','EPA','ESR','EZE','ENO','FAO','FBD','FCO','FDO','FLR','FLW','FMA',
                'FNC','FRA','FRS','FOR','FTE','GDL','GHU','GIB','GPO','GRU','GRW','GRX','GUA','GYE','HAJ','HAM','HAV','HBX','HEA','HEL','HGL',
                'HHN','HIR','HKG','HMO','HND','HOG','HOR','HNL','HOU','IBZ','ICN','IGR','INV','IPC','IQQ','IRJ','IST','IVL','JAA','JER','JFK',
                'JKL','JSR','JUJ','KBL','KDH','KEF','KGD','LAD','LAS','LAX','LCE','LEI','LEU','LGG','LGS','LGW','LHR','LIM','LIR','LIS','LTN',
                'LUQ','MAD','MCS','MDE','MDQ','MVD','MDZ','MEC','MGA','MTY','MEX','MDX','MFM','MIA','MKC','MLH','MLN','MPN','MUC','MXP',
                'MZR','MCO','NAP','NIC','NLU','NLK','OPO','ORA','ORD','ORK','ORY','OYA','PBR','PDP','PDL','PHL','PIX','PJC','PNA','PRA','PRQ',
                'PSY','PTY','PUJ','PUQ','PXO','QGY','QRC','QSA','RAK','RBA','RES','REU','RGA','RHD','RLO','RMU','ROS','RRG','RSA','RUH','SAL',
                'SAP','SBZ','SCU','SCL','SDE','SDQ','SFM','SFN','SIN','SJO','SJZ','SKG','SLA','SMA','SNU','SUF','SVO','SVQ','SXB','SYD','TER',
                'TFN','TFS','TGD','TGU','THF','TLS','TLV','TPE','TRS','TSE','TTG','TUR','UIO','USH','UZU','VCP','VDC','VDM','VIE','VKO','VLC',
                'VGO','VLL','VME','VVI','WLG','XRY','XPL','YFB','YHU','YHZ','YOW','YQB','YRB','YUL','YVM','YVR','YWG','YYY','YYZ','ZAG','ZAZ']

class VistaCrearTrayectos(Resource):

    def post(self):
        # Crea un trayecto en la aplicacion
        # Endpoint http://localhost:3002/routes/
        try:
            token = request.headers.get('Authorization', None)[7:]
            headers = {'Authorization': 'Bearer {0}'.format(token)}
            content = requests.get(
                'http://localhost:3000/users/me', headers=headers)

            if len(request.json['sourceAirportCode'].strip()) == 0:
                return {'mensaje': 'El código del origen del trayecto no puede estar vacío'}, 400

            if len(request.json['sourceCountry'].strip()) == 0:
                return {'mensaje': 'El origen del trayecto no puede estar vacío'}, 400

            if len(request.json['destinyAirportCode'].strip()) == 0:
                return {'mensaje': 'El código de destino del trayecto no puede estar vacío'}, 400

            if len(request.json['destinyCountry'].strip()) == 0:
                return {'mensaje': 'El destino del trayecto no puede estar vacío'}, 400

            if len(request.json['bagCost'].strip()) == 0:
                return {'mensaje': 'El costo de equipaje del trayecto no puede estar vacío'}, 400

            if request.json['sourceAirportCode'] not in AEROPUERTOS:
                return {'mensaje': 'El código del origen del trayecto no es válido'}, 400

            if request.json['destinyAirportCode'] not in AEROPUERTOS:
                return {'mensaje': 'El código de destino del trayecto no es válido'}, 400

            if content.status_code == 200:

                source = str(request.json['sourceAirportCode'])
                destination = request.json['destinyAirportCode']
                date = datetime.now()
                query = Trayecto.query
                query = query.filter(Trayecto.sourceAirportCode == source,
                                     Trayecto.destinyAirportCode == destination,
                                     Trayecto.createdAt <= date,
                                     Trayecto.createdAt >= (
                                         date - timedelta(days=30))
                                     )
                result = query.all()
                if len(result) > 0:
                    return {'mensaje': 'El trayecto ya existe ' + str(len(result)) + ' veces'}, 412

                else:
                    try:
                        new_trayecto = Trayecto(
                            sourceAirportCode=request.json['sourceAirportCode'],
                            sourceCountry=request.json['sourceCountry'],
                            destinyAirportCode=request.json['destinyAirportCode'],
                            destinyCountry=request.json['destinyCountry'],
                            bagCost=request.json['bagCost'],
                        )
                        db.session.add(new_trayecto)
                        db.session.commit()

                        return {'id': new_trayecto.id, 'createdAt': new_trayecto.createdAt.isoformat(timespec='seconds'), 'expireAt': (new_trayecto.createdAt + timedelta(days=30)).isoformat(timespec='seconds')}, 201

                    except Exception as e:
                        return {'mensaje': 'A ocurrido un error, por favor vuelve a intentar', 'error': str(e)}, 503

            else:
                return content.json(), 401

        except Exception as e:
            return {'mensaje': 'Por favor ingresar un token válido', 'error': str(e)}, 401


class VistaGetTrayectos(Resource):
    def get(self):
        # Busca un trayecto en la aplicacion
        # Endpoint http://localhost:3002/routes...

        try:
            token = request.headers.get('Authorization', None)[7:]
            headers = {'Authorization': 'Bearer {0}'.format(token)}
            content = requests.get(
                'http://localhost:3000/users/me', headers=headers)

            if content.status_code == 200:

                source = request.args.get('from', type=str)
                destination = request.args.get('to', type=str)
                date = request.args.get('when', type=toDate)
                query = Trayecto.query

                if source:
                    query = query.filter(Trayecto.sourceAirportCode == source)
                if destination:
                    query = query.filter(
                        Trayecto.destinyAirportCode == destination)
                if date:
                    if str(type(date)) == "<class 'datetime.date'>":
                        query = query.filter(Trayecto.createdAt <= date)
                    else:
                        return {'mensaje': 'La fecha introducida no está en formato fecha'}, 400
                if date:
                    query = query.filter(
                        Trayecto.createdAt >= (date - timedelta(days=30)))

                result = query.all()
                return [trayecto_schema_list.dump(al) for al in result], 200

            else:
                return content.json(), 401

        except Exception as e:
            return {'mensaje': 'Por favor ingresar un token válido', 'error': str(e)}, 401


class VistaGetTrayecto(Resource):
    def get(self, route_id):
        # Busca un trayecto en la aplicacion
        # Endpoint http://localhost:3002/routes/{id}

        try:
            token = request.headers.get('Authorization', None)[7:]
            headers = {'Authorization': 'Bearer {0}'.format(token)}
            content = requests.get(
                'http://localhost:3000/users/me', headers=headers)

            if content.status_code == 200:

                trayecto = Trayecto.query.filter(
                    Trayecto.id == route_id).first()

                if trayecto == None:
                    return {'mensaje': 'No existe trayecto con ese identificador'}, 404
                return trayecto_schema_list.dump(trayecto)
            else:
                return content.json(), 401

        except Exception as e:
            return {'mensaje': 'Por favor ingresar un token válido', 'error': str(e)}, 401


class VistaPong(Resource):

    def get(self):
        # Retorna pong
        # Endpoint http://localhost:3002/routes/ping
        return 'pong', 200


class ViewTrayectos(Resource):
    def get(self):
        # Retorna todos los usuarios registrados
        # Endpoint http://localhost:3002/users/all
        return [trayecto_schema_list.dump(trayecto) for trayecto in Trayecto.query.all()]


def toDate(dateString):
    return datetime.strptime(dateString, "%d/%m/%Y").date()