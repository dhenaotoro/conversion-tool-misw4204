from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from datetime import datetime
from flask import jsonify
import re
import hashlib

from modelos import db, Usuario

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
            contrasena_encriptada = hashlib.md5(request.json["password1"].encode('utf-8')).hexdigest()
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
        contrasena_encriptada = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.nombre == request.json["username"],
                                       Usuario.contrasena == contrasena_encriptada).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"token": token_de_acceso}