from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from datetime import datetime
from flask import jsonify
import re
import hashlib
import moviepy.editor as moviepy

from modelos import db, Usuario, Archivo, ArchivoSchema
#from tareas import convertir_archivos

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
          - Debe tener 6 caracteres.
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
        archivo_as_json = "SIN JSON"
        try:
            nombreArchivo = request.json["fileName"]
            nuevoFormato = request.json["newFormat"]
            tiempoActual = datetime.now()
            marcaTiempo = tiempoActual.strftime("%Y-%m-%d %H:%M:%S")
            estado = "uploaded"

            nombre_archivo_separado_por_punto = request.json["fileName"].split('.')
            ruta_y_nombre_archivo = nombre_archivo_separado_por_punto[0]
            extension_archivo_origen = nombre_archivo_separado_por_punto[1]
            if re.match(r'./videos/origen/', ruta_y_nombre_archivo):
              return {"mensaje": "El video debe ser guardado en la ruta ./videos/origen/."}, 500
            if not extension_archivo_origen in {"mp4", "webm", "avi"}:
              return {"mensaje": "El formato del video a convertir debe ser entre avi, mp4 o webm."}, 500
            if extension_archivo_origen == nuevoFormato:
              return {"mensaje": f"Se debe elegir un formato destino distinto al formato del video original"}, 500
            if not nuevoFormato in {"mp4", "webm", "avi"}:
              return {"mensaje": "El formato debe ser entre avi, mp4 o webm. Los formatos mpeg y wmv aun no son soportados"}, 500

            archivo = Archivo(
                marcaTiempo=marcaTiempo,
                estado=estado,
                nombreArchivo=nombreArchivo,
                nuevoFormato=nuevoFormato
            )
            db.session.add(archivo)
            db.session.commit()

            #archivos = Archivo.query.filter_by(estado='uploaded').all()
            #archivos_a_retornar = []
            #archivo_schema = ArchivoSchema()
            #for archivo in archivos:
            #  archivo_as_json = archivo_schema.dump(archivo)
            #  archivos_a_retornar.append(archivo_as_json)
            #  convertir_archivos.delay(archivo_as_json)

            #return {"mensaje": "Archivo cargo correctamente", "archivos_schema": archivos_a_retornar}, 201
            return {"mensaje": "Archivo cargo correctamente"}, 201
        except Exception as e:
            return {"mensaje": "Error: " + str(e), "archivo_schema": archivo_as_json}, 500

    @jwt_required()
    def get(self):
        try:
            max = request.args.get('max', default=10, type=int)
            order = request.args.get('order', default=0, type=int)
            archivos = Archivo.query.limit(max)
            archivoArreglo = []
            for archivo in archivos:
                archivoArreglo.append({
                    'id': archivo.id,
                    'marcaTiempo': archivo.marcaTiempo.strftime('%Y-%m-%d %H:%M:%S'),
                    'estado': archivo.estado,
                    'nombreArchivo': archivo.nombreArchivo,
                    'nuevoFormato': archivo.nuevoFormato
                })
            if order == 0:
                archivoArreglo.sort(key=lambda task: task['id'])
            elif order == 1:
                archivoArreglo.sort(key=lambda task: task['id'], reverse=True)
            return jsonify(archivoArreglo)
        except Exception as e:
            return {"message": "Error: " + str(e)}, 500
        
class VistaArchivos(Resource):

  @jwt_required()
  def get(self, id_task):
    response = {}
    try:
      if id_task != None:
        tarea = Archivo.query.filter_by(id=id_task).first()
        if tarea:
          response = {
            "mensaje": "Datos encontratos",
            "tarea": {
              "Estado": str(tarea.estado),
              "Url original": str(tarea.nombreArchivo),
              "Url convertido": str(tarea.urlArchivo),
            }
          }, 201
        else:
          response = { "mensaje": """No existe una tarea con id {}""".format(str(id_task)) }, 409
      else:
        response = { "mensaje": """El id {} ingresado no es valido""".format(str(id_task)) }, 409
    except Exception as error:
      response = { "mensaje": "Error: " + str(error) }, 500
    finally:
      return response
  
  @jwt_required()
  def delete(self, id_task):
    response = {}
    try:
      if id_task != None:
        tarea = Archivo.query.filter_by(id=id_task).first()
        if tarea:
          tareaEliminar = Archivo.query.get_or_404(tarea.id)
          db.session.delete(tareaEliminar)
          db.session.commit()
          response = { "mensaje": """La tarea con id {} se elimino correctamente""".format(str(id_task)) }, 201
        else:
          response = { "mensaje": """No existe una tarea con id {}""".format(str(id_task)) }, 409
      else:
        response = { "mensaje": """El id {} ingresado no es valido""".format(str(id_task)) }, 409
    except Exception as error:
      response = { "mensaje": "Error: " + str(error) }, 500
    finally:
      return response
