from flask import request, Response
from data.models import movie, User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from recursos.errors import SchemaValidationError, MovieAlreadyExistsError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError, InternalServerError


class MoviesApi(Resource):
    def get(self):
        movies = movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            pelicula = movie(**body, anadido_por=user)
            pelicula.save()
            user.update(push__movies=pelicula)
            user.save()
            id = pelicula.id
            return {'id':str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError
    
class MovieApi(Resource):
    def get(self, indice):
        movies = movie.objects.get(id=indice).to_json()
        return Response(movies, mimetype='application/json',status=200)
        try:
            peliculas = movie.objects.get(id=indice).to_json()
            return Response(peliculas, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError

    @jwt_required
    def put(self, indice):
        try:
            user_id = get_jwt_identity()
            pelicula = movie.objects.get(id=indice, anadido_por=user_id)
            body = request.get_json()
            movie.objects.get(id=indice).update(**body)
            return 'editado', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, indice):
        try:
            user_id = get_jwt_identity()
            pelicula = movie.objects.get(id=indice, anadido_por=user_id)
            pelicula.delete()
            return 'deleted', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError
