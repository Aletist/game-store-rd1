from unittest import mock


def test_add_user(client, token_auth):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    r = client.post('/users/', json={'user': user})
    status_code1 = r.status_code

    resp = client.get('/user/1', headers=token_auth)

    expected = user.copy()
    expected.update({'user_id': mock.ANY})
    expected['is_active'] = True

    r = client.post('/users/', json={'user': user})
    status_code2 = r.status_code
    assert status_code1 == 201 and status_code2 == 409 and resp.json == expected


def test_update_user(client, token_auth):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    client.post('/users/', json={'user': user}, headers=token_auth)

    new_data = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
    client.put('/user/1', json=new_data, headers=token_auth)

    new_data['is_active'] = True
    new_data['user_id'] = 1
    resp = client.get('/user/1', headers=token_auth)
    assert new_data == resp.json


def test_list_users(client, token_auth):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    user2 = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}

    client.post('/users/', json={'user': user1}, headers=token_auth)
    client.post('/users/', json={'user': user2}, headers=token_auth)

    admin_user = {'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'is_active': True}
    admin_user['user_id'] = 0
    user1['user_id'] = 1
    user2['user_id'] = 2
    user1['is_active'] = True
    user2['is_active'] = True

    resp = client.get('/users/', headers=token_auth)
    assert resp.json == {'0': admin_user, '1': user1, '2': user2}


def test_delete_user(client, token_auth):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    client.post('/users/', json={'user': user}, headers=token_auth)

    resp = client.delete('/user/1', headers=token_auth)
    assert resp.status_code == 204

    resp = client.get('/user/1', headers=token_auth)
    assert resp.status_code == 404


def test_search_user(client, user_data, token_auth):

    for u in user_data:
        client.post('/users/', json={'user': u})

    resp = client.get('search/name/Ivan', headers=token_auth)

    user_data[1]['is_active']=True
    user_data[1]['user_id']=mock.ANY

    expected_users = [user_data[1]]
    assert resp.json == expected_users
