from flask import Blueprint, g
from flask_restful import Api, Resource, abort

from . import get_auth_token


class LoginHandler(Resource):

    def post(self):
        try:
            return {'token': get_auth_token()}
        except Exception:
            abort(404)

class LogoutHandler(Resource):
    def post(self):
        g.user = None
        return '', 200


def register_handlers(app):

    bp = Blueprint('auth', 'AUTHENTICATION')

    api = Api(bp)
    api.add_resource(LoginHandler, '/login')
    api.add_resource(LogoutHandler, '/logout')

    app.register_blueprint(bp)

    return api
