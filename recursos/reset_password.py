from flask import request, render_template
from flask_jwt_extended import create_access_token, decode_token
from data.models import User
from flask_restful import Resource
import datetime
from recursos.errors import SchemaValidationError, InternalServerError, EmailDoesNotExistsError, BadTokenError, ExpiredTokenError
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from services.mail_service import send_email

class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError

            user = User.objects.get(email=email)
            if not user:
                raise EmailDoesNotExistsError

            expires = datetime.timedelta(hours=3)
            reset_token = create_access_token(str(user.id), expires_delta = expires)

            return send_email('[Movie-bag] Reset password', 
            sender = 'support@movie-bag.cl', 
            text_body = render_template('email/reset_password.txt', url = url + reset_token), 
            html_body = render_template('email/rest_password.html', url = url + reset_token))
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailDoesNotExistsError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError
            
            user_id = decode_token(reset_token)['identity']

            user = User.objects.get(id=user_id)
            user.modify(password=password)
            user.hash_password()

            return send_email('[Movie-bag] Password reset successful',
                              sender='support@movie-bag.cl',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError:
            raise SchemaValidationError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError
