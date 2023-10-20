from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from datetime import datetime
from flask import jsonify
import re
import hashlib
import datetime

from modelos import db, Usuario, Archivo

class VistaSignUp(Resource):

  def post(self):
    usuario = Usuario.query.filter(Usuario.nombre == request.json["username"]).first()
    if usuario is None:
      if request.json["password1"] != request.json["password2"]:
        return {"mensaje": "Las contraseñas no son iguales"}, 500
      elif not re.search(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{6}$", request.json["password1"]):
        return {"mensaje": """La contraseña debe cumplir con los siguientes criterios:
          - Debe tener al menos una letra en mayúscula.
          - Debe tener al menos un número.
          - Debe tener al menos un caracter especial.
        """}, 500
      contrasena_encriptada = hashlib.md5(request.json["password1"].encode("utf-8")).hexdigest()
      nuevo_usuario = Usuario(nombre=request.json["username"], contrasena=contrasena_encriptada, email=request.json["email"])
      db.session.add(nuevo_usuario)
      db.session.commit()
      return {"mensaje": "cuenta creada exitosamente", "id": nuevo_usuario.id}, 200
    else:
      if usuario.email == request.json["email"]:
        return {"mensaje": "El email ya existe"}, 409
      elif usuario.nombre == request.json["username"]:
        return {"mensaje": "El usuario ya existe"}, 409
            
class VistaLogin(Resource):

  def post(self):
    contrasena_encriptada = hashlib.md5(request.json["password"].encode("utf-8")).hexdigest()
    usuario = Usuario.query.filter(Usuario.nombre == request.json["username"], Usuario.contrasena == contrasena_encriptada).first()
    db.session.commit()
    if usuario is None:
      return "El usuario no existe", 404
    else:
      token_de_acceso = create_access_token(identity=usuario.id)
      return {"token": token_de_acceso}

class VistaArchivo(Resource):
  @jwt_required()
  def post(self):
    try:
      nombreArchivo = request.json["fileName"]
      nuevoFormato = request.json["newFormat"]
      tiempoActual = datetime.datetime.now()
      marcaTiempo = tiempoActual.strftime("%Y-%m-%d %H:%M:%S")
      estado = "uploaded"
      print("Prueba "+nombreArchivo)

      # Create an instance of the Archivo model and set its attributes
      archivo = Archivo(
        marcaTiempo=marcaTiempo,
        estado=estado,
        nombreArchivo=nombreArchivo,
        nuevoFormato=nuevoFormato
      )

      # Add the instance to the SQLAlchemy session and commit it to the database
      db.session.add(archivo)
      db.session.commit()

      # Return a success response
      return {"mensaje": "Archivo cargo correctamente"}, 201
    except Exception as e:
      # Handle any exceptions, and return an error response if necessary
      return {"mensaje": "Error: " + str(e)}, 500
    
class VistaArchivos(Resource):
          
  def get(self, id_task):
    response = {}
    try:
      if id_task != None:
        # Nombre archivo
        # Estado
        # Url de descarga archivo original
        # Url de descarga archivo convertido
        tarea = Archivo.query.filter_by(id=id_task).first()
        response = {
          "mensaje": "Datos encontratos",
          "tarea": {
            "Nombre": str(tarea.nombreArchivo),
            "Estado": str(tarea.estado),
            "Url original": str(tarea.urlArchivoOriginal),
            "Url convertido": str(tarea.urlArchivoConvertido),
          }
        }, 201
      else:
        response = { "mensaje": """No existe una tarea con id {}""".format(str(id_task)) }, 409
    except Exception as error:
      response = { "mensaje": "Error: " + str(error) }, 500
    finally:
      return response
        
  def delete(self, id_task):
    try:
      print("ID DELETE: ", str(id_task))
      return "Test"
    except Exception as error:
      return "Error"