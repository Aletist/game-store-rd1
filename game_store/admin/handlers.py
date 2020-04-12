from flask_restful import Resource, Api, abort
from flask import current_app, request, g

from ..auth import auth


class UserHandler(Resource):

    @auth.login_required
    def get(self, user_id):

        # current_app.auth_checker.check('Users', 'read', g.user['user_id'])
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if not user['is_active']:
                abort(404)
            return user
        except KeyError:
            abort(404)

    def put(self, user_id):
        data = request.get_json()
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if not user['is_active']:
                abort(400)

            for key in data.keys():
                user[key] = data[key]
        except KeyError:
            abort(400)

    def delete(self, user_id):
        try:
            user = current_app.db['users'].get_by_id(user_id)
            user['is_active'] = False
            return '', 204
        except KeyError:
            abort(400)


class UserListHandler(Resource):

    @auth.login_required
    def get(self):
        return current_app.db['users'].storage


    # TODO implement error 409 when trying to add same user twice.
    @auth.login_required
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['is_active'] = True
        current_app.db['users'].insert(data)
        return '', 201


class UserSearcher(Resource):

    def get(self, key, value):
        try:
            return current_app.db['users'][key].fetchall(lambda x: x == value)
            # return [user for user
            #         in current_app.db['users'].storage.values()
            #         if user['is_active'] and user[key] == value]
        except KeyError:
            abort(400)


def register_handlers(app):
    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserSearcher, '/search/<key>/<value>')

    return api
