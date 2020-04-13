from flask_restful import Resource, Api, abort
from flask import current_app, request, g, jsonify

from ..auth import auth


class UserHandler(Resource):

    @auth.login_required
    def get(self, user_id):

        current_app.auth_checker.check('Users', 'read', g.user['user_id'])
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if not user['is_active']:
                abort(404)
            return user
        except KeyError:
            abort(404)

    @auth.login_required
    def put(self, user_id):
        current_app.auth_checker.check('Users', 'update', g.user['user_id'])
        data = request.get_json()
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if not user['is_active']:
                abort(400)

            for key in data.keys():
                user[key] = data[key]
        except KeyError:
            abort(400)

    @auth.login_required
    def delete(self, user_id):
        current_app.auth_checker.check('Users', 'delete', g.user['user_id'])
        user = current_app.db['users'].get_by_id(user_id)
        user['is_active'] = False
        return '', 204



class UserListHandler(Resource):

    @auth.login_required
    def get(self):
        current_app.auth_checker.check('Users', 'list', g.user['user_id'])
        return current_app.db['users'].storage

    @auth.login_required
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['is_active'] = True
        if current_app.db['users'].email.fetchone(lambda x: x == data['email']):
            abort(409)
        current_app.db['users'].insert(data)
        return '', 201

class UserRegisterHandler(Resource):
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['is_active'] = True
        if current_app.db['users'].email.fetchone(lambda x: x == data['email']):
            abort(409)
        current_app.db['users'].insert(data)
        return '', 201


class UserSearcher(Resource):

    def get(self, key, value):
        try:
            return list(getattr(current_app.db['users'], key).fetchall(lambda x: x == value))
        except KeyError:
            abort(400)


def register_handlers(app):
    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserRegisterHandler, '/register/')
    api.add_resource(UserSearcher, '/search/<key>/<value>')

    return api
