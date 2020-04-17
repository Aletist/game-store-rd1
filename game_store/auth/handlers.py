from flask import Blueprint, g, request, current_app
from flask_restful import Api, Resource, abort

from . import get_auth_token, encode_auth_token, auth


class LoginHandler(Resource):

    def post(self):
        try:
            return {'token': get_auth_token()}
        except Exception:
            abort(404)


class UserRegisterHandler(Resource):
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['is_active'] = True
        '''
        QUESTION: should we be able to re-register accounts using inactive accounts` unique fields?
        '''
        if current_app.db['users'].email.fetchone(lambda x: x == data['email']):
            abort(409)
        current_app.db['users'].insert(data)
        g.user = data
        config = current_app.config
        token = encode_auth_token(g.user['username'], config).decode()
        return {'token': token}, 201


class LogoutHandler(Resource):
    @auth.login_required
    def post(self):
        config = current_app.config

        token = encode_auth_token(g.user['email'], config, True).decode()
        return {'token': token}


def register_handlers(app):

    bp = Blueprint('auth', 'AUTHENTICATION')

    api = Api(bp)
    api.add_resource(LoginHandler, '/login')
    api.add_resource(UserRegisterHandler, '/register')
    api.add_resource(LogoutHandler, '/logout')

    app.register_blueprint(bp)

    return api