from flask import Flask
from flask_restful import Api
from recursos.errors import errors
from data.db import initialize_db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION') #'ENV_FILE_LOCATION' -> export ENV_FILE_LOCATION = ./.env
mail = Mail(app)
from recursos.routes import init_routes
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb://localhost/movie-bag'
# }

initialize_db(app)
init_routes(api)

