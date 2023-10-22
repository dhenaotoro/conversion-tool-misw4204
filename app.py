from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db
from vistas import VistaArchivo, VistaArchivos, VistaLogin, VistaSignUp, VistaLogin
from flask import Flask
from sqlalchemy.exc import OperationalError
import time

class Config:

    @staticmethod
    def init():
        app = Flask(__name__)

        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/conversion_tool"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["JWT_SECRET_KEY"] = "frase-secreta"
        app.config["PROPAGATE_EXCEPTIONS"] = True

        app_context = app.app_context()

        return (app, app_context)
    
def connect_to_database_with_retry(app_context, maximo_intentos=5, intervalo_reintento=3):
        reintentos = 0
        while reintentos < maximo_intentos:
            try:
                db.init_app(app)
                app_context.push()
                db.create_all()
                return
            except OperationalError:
                # conexion fallida, esperar y luego reintentar
                time.sleep(intervalo_reintento)
                reintentos += 1
        # Si los maximos intentos se alcanzaron sin una conexion exitosa, levante un error
        raise Exception("Fallo al conectarse a la base de datos.")

(app, app_context) = Config.init()
connect_to_database_with_retry(app_context)

api = Api(app)
api.add_resource(VistaSignUp, "/api/auth/signup")
api.add_resource(VistaLogin, "/api/auth/login")
api.add_resource(VistaArchivo, "/api/tasks")
api.add_resource(VistaArchivos, "/api/tasks/<int:id_task>")
jwt = JWTManager(app)
