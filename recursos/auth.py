from flask import request, Response
from data.models import User
from flask_restful import Resource
import datetime
from flask_jwt_extended import create_access_token
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from recursos.errors import SchemaValidationError, InternalServerError, EmailAlreadyExistsError, UnauthorizedError


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id':str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError

class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            autorizado = user.check_password(body.get('password'))
            if not autorizado:
                raise UnauthorizedError
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError