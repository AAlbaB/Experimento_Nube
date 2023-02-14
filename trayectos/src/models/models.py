from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, Schema
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Trayecto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sourceAirportCode = db.Column(db.String(3), nullable = False)
    sourceCountry = db.Column(db.String(128), nullable = False)
    destinyAirportCode = db.Column(db.String(3), nullable = False)
    destinyCountry = db.Column(db.String(128), nullable=False)
    bagCost = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    createdAt = db.Column(db.DateTime, default = datetime.now())

class TrayectoSchemaList(SQLAlchemySchema):
    class Meta:
        model = Trayecto
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.Integer()
    sourceAirportCode = fields.String()
    sourceCountry = fields.String()
    destinyAirportCode = fields.String()
    destinyCountry = fields.String()
    bagCost = fields.String()
