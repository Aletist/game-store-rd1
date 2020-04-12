import base64

from game_store.auth.token import decode_auth_token


def test_login_with_email_password(client):

    username = 'admin@gov.ua'
    auth_str = base64.b64encode(':'.join([username, 'S3cPa55w0rd!']).encode("latin-1"))
    headers = {
        'Authorization': b'Basic ' + auth_str
    }
    auth_resp = client.post('/login', headers=headers)
    status_code = auth_resp.status_code

    token = auth_resp.json['token']
    user_data = decode_auth_token(token.encode(), client.application.config)

    assert status_code == 200 and user_data == username
