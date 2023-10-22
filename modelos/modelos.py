from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, DateTime

db = SQLAlchemy()

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(50))
  contrasena = db.Column(db.String(50))
  email = db.Column(db.String(50))

class Archivo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  marcaTiempo = Column(DateTime)
  estado = db.Column(db.String(50))
  nombreArchivo = db.Column(db.String(500))
  nuevoFormato = db.Column(db.String(50))
  urlArchivo = db.Column(db.String(500), default="")

class UsuarioSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Usuario
    load_instance = True
      
  id = fields.String()

class ArchivoSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Archivo
    load_instance = True
      
  id = fields.String()
  marcaTiempo = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
  estado = fields.String()
  nombreArchivo = fields.String()
  nuevoFormato = fields.String()
  urlArchivo = fields.String()

   