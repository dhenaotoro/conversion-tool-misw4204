from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import db
from vistas import VistaSignUp, VistaLogin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/conversion_tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.session.commit()
db.create_all()

api = Api(app)
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogin, '/api/auth/login')

jwt = JWTManager(app)