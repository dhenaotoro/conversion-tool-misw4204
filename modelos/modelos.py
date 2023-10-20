from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Date

db = SQLAlchemy()

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(50))
  contrasena = db.Column(db.String(50))
  email = db.Column(db.String(50))

class UsuarioSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Usuario
    load_instance = True
      
  id = fields.String()

class Archivo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  marcaTiempo = Column(Date)
  estado = db.Column(db.String(50))
  nombreArchivo = db.Column(db.String(50))
  nuevoFormato = db.Column(db.String(50))
  urlArchivoOriginal = db.Column(db.String(500))
  urlArchivoConvertido = db.Column(db.String(500), default="")
   