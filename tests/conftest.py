from pytest import fixture

from game_store.admin.app import create_app
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
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!'})
        yield c

@fixture()
def token_auth(config):

    username = 'admin@gov.ua'
    token = encode_auth_token(username, config)
    return {
        'Authorization': b'Bearer ' + token
    }