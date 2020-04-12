# from pytest import fixture
# from unittest import mock
#
# from game_store.admin.app import create_app
# from game_store.auth.token import encode_auth_token
#
#
# @fixture()
# def app_config():
#
#     return {
#         'JWT_SECRET_KEY': 'ASDFGHJKL:ZX',
#         'JWT_TTL_SECONDS': 500
#     }
#
#
# @fixture(scope='function')
# def client(app_config):
#
#     app = create_app('Test-Game-Store')
#     app.config.from_mapping(app_config)
#     with app.test_client() as c:
#         c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!'})
#         yield c
#
#
# @fixture()
# def token_auth(app_config):
#
#     username = 'admin@gov.ua'
#     token = encode_auth_token(username, app_config)
#     return {
#         'Authorization': b'Bearer ' + token
#     }
#
#
# def test_add_user(client, token_auth):
#     user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
#     client.post('/users/', json={'user': user}, headers=token_auth)
#     resp = client.get('/user/1', headers=token_auth)
#
#     expected = user.copy()
#     expected.update({'user_id': mock.ANY})
#     expected['is_active'] = True
#
#     status_code = resp.status_code
#     assert status_code == 200 and resp.json == expected
#
#
# def test_update_user(client):
#     user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
#     client.post('/users/', json={'user': user})
#
#     new_data = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
#     client.put('/user/0', json=new_data)
#
#     new_data['is_active'] = True
#     resp = client.get('/user/0')
#     assert new_data == resp.json
#
#
# def test_list_users(client):
#     user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
#
#     client.post('/users/', json={'user': user1}, headers=token_auth)
#     resp = client.get('/user/1', headers=token_auth)
#
#     expected = user1.copy()
#     expected.update({'user_id': mock.ANY})
#
#     status_code = resp.status_code
#     assert status_code == 200 and resp.json == expected
#     user2 = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
#
#     client.post('/users/', json={'user': user1})
#     client.post('/users/', json={'user': user2})
#
#     user1['is_active'] = True
#     user2['is_active'] = True
#
#     resp = client.get('/users/')
#     assert resp.json == {'0': user1, '1': user2}
#
#
# def test_delete_user(client):
#     user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
#     client.post('/users/', json={'user': user})
#
#     resp = client.delete('/user/0')
#     assert resp.status_code == 204
#
#     resp = client.get('/user/0')
#     assert resp.status_code == 404
#
#
# def test_delete_nonexistent_user(client):
#     resp = client.delete('/user/9')
#     assert resp.status_code == 400
#
#
# def test_search_user(client):
#     user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
#     user2 = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
#     user3 = {'name': "Ivan", 'surname': "Langobard", 'email': "vania2@mail.com"}
#
#     client.post('/users/', json={'user': user1})
#     client.post('/users/', json={'user': user2})
#     client.post('/users/', json={'user': user3})
#
#     resp = client.get('search/name/Ivan')
#
#     user1['is_active'] = True
#     user2['is_active'] = True
#     user3['is_active'] = True
#
#     expected_users = [user2, user3]
#     assert resp.json == expected_users
