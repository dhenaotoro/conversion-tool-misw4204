from flask import Flask
#from flask_jwt_extended import JWTManager
from flask_restful import Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '' #Connection postgres
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaSignIn, '/signin')

@app.route("/")
def helloWord():
    return "Hello world"