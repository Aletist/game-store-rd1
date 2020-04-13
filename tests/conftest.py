from pytest import fixture

from game_store.admin.app import create_app
from game_store.admin.db import create_db
from game_store.admin.models import Users
from game_store.auth import encode_auth_token


@fixture(scope='function')
def config():
    return {
        'JWT_TTL_SECONDS': 300,
        'JWT_SECRET_KEY': '12345677890'
    }


@fixture(scope='function')
def client(config):
    app = create_app('Test')
    app.config.from_mapping(config)
    # todo: make something fancy here
    with app.test_client() as c:
        admin_user = {'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'is_active': True}
        c.application.db['users'].insert(admin_user)
        c.application.db['roles'].insert({'name': 'admin'})
        c.application.db['user-roles'].insert({'user': 0, 'role': 0})
        c.application.db['resources'].insert({'name': 'Users'})
        c.application.db['perms'].insert({'resource': 0, 'action': 'read'})
        c.application.db['perms'].insert({'resource': 0, 'action': 'list'})
        c.application.db['perms'].insert({'resource': 0, 'action': 'add'})
        c.application.db['perms'].insert({'resource': 0, 'action': 'update'})
        c.application.db['perms'].insert({'resource': 0, 'action': 'delete'})
        c.application.db['role-perms'].insert({'role': 0, 'perm': 0})
        c.application.db['role-perms'].insert({'role': 0, 'perm': 1})
        c.application.db['role-perms'].insert({'role': 0, 'perm': 2})
        c.application.db['role-perms'].insert({'role': 0, 'perm': 3})
        c.application.db['role-perms'].insert({'role': 0, 'perm': 4})

        yield c


@fixture(scope='function')
def token_auth(config):
    username = 'admin@gov.ua'
    token = encode_auth_token(username, config)
    return {
        'Authorization': b'Bearer ' + token
    }


@fixture(scope='function')
def user_data():
    return [{
        'name': 'Taras',
        'surname': 'Shevchenko',
        'email': 'taras@shevchenko.name',
        'password': 'Zapovit2.0'
    }, {
        'name': 'Ivan',
        'surname': 'Franko',
        'email': 'ivan@franko.name',
        'password': 'Kamenyar123'
    }, {
        'name': 'Lesya',
        'surname': 'Ukrainka',
        'email': 'lesya@ukrainka.name',
        'password': 'Mavka789'
    }]


@fixture(scope='function')
def role_data():
    return [{
        'name': 'admin'
    }, {
        'name': 'user'
    }, {
        'name': 'manager'
    }]


@fixture(scope='function')
def user_role_data():
    return [{
        'user': 1,
        'role': 0
    }, {
        'user': 2,
        'role': 1
    }, {
        'user': 3,
        'role': 2
    }]


@fixture(scope='function')
def users_db(user_data):
    users = Users()
    for u in user_data:
        users.insert(u)
    return users

#
# @fixture()
# def test_db(client, user_data, role_data):
#     db = client.application.db
#     for b in db:
#         users.insert(u)
#     return users
