from flask import Flask
#from flask_cors import CORS
#from flask_jwt_extended import JWTManager
#from flask_restful import Api

app = Flask(__name__)

@app.route("/")
def helloWord():
    return "Hello world"