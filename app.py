from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db
from vistas import VistaArchivo, VistaArchivos, VistaLogin, VistaSignUp, VistaLogin
from sqlalchemy.exc import OperationalError
import time

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/conversion_tool"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "frase-secreta"
app.config["PROPAGATE_EXCEPTIONS"] = True

def connect_to_database_with_retry(db_uri, max_retries=5, retry_interval=5):
  retries = 0
  while retries < max_retries:
    try:
      db.init_app(app)
      with app.app_context() as app_context:
        app_context.push()
        db.create_all()
        return
    except OperationalError:
      # Connection failed, wait and then retry
      time.sleep(retry_interval)
      retries += 1

  # If max retries reached without a successful connection, raise an error
  raise Exception("Failed to connect to the database.")

connect_to_database_with_retry(app.config["SQLALCHEMY_DATABASE_URI"])

api = Api(app)
api.add_resource(VistaSignUp, "/api/auth/signup")
api.add_resource(VistaLogin, "/api/auth/login")
api.add_resource(VistaArchivo, "/api/tasks")
api.add_resource(VistaArchivos, "/api/tasks/<int:id_task>")
jwt = JWTManager(app)
