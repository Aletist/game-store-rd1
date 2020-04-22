from flask_restful import Resource, Api, abort
from flask import current_app, request, g

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
            return '', 200
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


class UserSearcher(Resource):

    def get(self, key, value):
        try:
            return list(getattr(current_app.db['users'], key).fetchall(lambda x: x == value))
        except KeyError:
            abort(400)


class RoleHandler(Resource):
    @auth.login_required
    def get(self, role_name):
        current_app.auth_checker.check('Roles', 'read', g.user['user_id'])
        role = current_app.db['roles'].name.fetchone(lambda x: x == role_name)
        if not role:
            abort(404)
        perm_ids = [item['role-permission_id'] for item
                    in current_app.db['role-perms'].name.fetchone(lambda x: x == role['role_id'])]
        permissions = [current_app.db['perms'].get_by_id(id) for id in perm_ids]
        return {
            'name': role['name'], 'permissions': permissions
        }

    @auth.login_required
    def put(self, role_name):
        current_app.auth_checker.check('Roles', 'update', g.user['user_id'])
        role = current_app.db['roles'].name.fetchone(lambda x: x == role_name)
        if not role:
            abort(400)
        try:
            role['name'] = request.get_json()['new_name']
            return '', 200
        except KeyError:
            abort(400)

    @auth.login_required
    def post(self, role_name):
        current_app.auth_checker.check('Roles', 'add', g.user['user_id'])
        data = {'name': role_name}
        current_app.db['roles'].insert(data)
        return '', 201


class RoleListHandler(Resource):
    @auth.login_required
    def get(self):
        current_app.auth_checker.check('Roles', 'list', g.user['user_id'])
        return current_app.db['roles'].values()


class UserRoleHandler(Resource):

    @auth.login_required
    def get(self, username):
        current_app.auth_checker.check('Users', 'list', g.user['user_id'])
        current_app.auth_checker.check('Roles', 'list', g.user['user_id'])
        role_ids = [item['role'] for item in current_app.db['user-roles'].user.fetchall(lambda x: x == username)]
        roles = current_app.db['roles'].role_id.fetchall(lambda x: x in role_ids)

        return {'username': username, 'roles': roles}


    @auth.login_required
    def put(self, username):
        current_app.auth_checker.check('Users', 'edit', g.user['user_id'])
        user = current_app.db['users'].name.fecthone(lambda x: x == username)['user_id']
        roles_update = request.get_json('upd_roles')
        for item in roles_update:
            if not current_app.db['roles'].role_id.fetchone(lambda x: x == item['role']):
                abort(400)

            temp = None
            for user_role in current_app.db['user-roles'].role.fetchall(lambda x: x == item['role']):
                if user_role['user'] == username:
                    temp = user_role
                    break
            if item['is_to_add']:
                if temp:
                    abort(409)
                current_app.db['user-roles'].insert({'user': user, 'role': item['role']})
            else:
                try:
                    del current_app.db['user-roles'][temp['user-role_id']]
                except TypeError:
                    pass


def register_handlers(app):
    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users')
    api.add_resource(UserSearcher, '/search/<key>/<value>')
    api.add_resource(RoleHandler, '/role/<string:role_name>')
    api.add_resource(RoleListHandler, '/roles')
    api.add_resource(UserRoleHandler, '/user_roles/<string:username>')

    return api
