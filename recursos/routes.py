from .movies import MoviesApi, MovieApi
from .auth import SignupApi, LoginApi
from .reset_password import ForgotPassword, ResetPassword

def init_routes(api):
    api.add_resource(MoviesApi, '/movies')
    api.add_resource(MovieApi, '/movie/<indice>')

    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')

    api.add_resource(ForgotPassword, '/auth/forgot')
    api.add_resource(ResetPassword, '/auth/reset')