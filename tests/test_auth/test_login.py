import base64
from pytest import fixture

from game_store.admin.app import create_app
from game_store.auth.token import decode_auth_token


@fixture()
def app_config():

    return {
        'JWT_SECRET_KEY': '12345677890',
        'JWT_TTL_SECONDS': 300
    }


@fixture(scope='function')
def client(app_config):

    app = create_app('Test-Auth')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'name': 'Root', 'email': 'root@example.com', 'password': 'Qwerty12344556'})
        yield c


def test_login_with_email_password(client):

    username = 'root@example.com'
    auth_str = base64.b64encode(':'.join([username, 'Qwerty12344556']).encode("latin-1"))
    headers = {
        'Authorization': b'Basic ' + auth_str
    }
    auth_resp = client.post('/login', headers=headers)
    status_code = auth_resp.status_code

    token = auth_resp.json['token']
    user_data = decode_auth_token(token.encode(), client.application.config)

    assert status_code == 200 and user_data == username
