from pytest import fixture

from game_store.admin.app import create_app


@fixture(scope='function')
def client():
    app = create_app('Test-Game-Store')
    with app.test_client() as c:
        yield c


def test_add_user(client):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    resp = client.post('/users/', json={'user': user})
    assert resp.status_code == 201

    user['is_active'] = True
    resp = client.get('/user/0')
    assert user == resp.json


def test_update_user(client):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    client.post('/users/', json={'user': user})

    new_data = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
    client.put('/user/0', json=new_data)

    new_data['is_active'] = True
    resp = client.get('/user/0')
    assert new_data == resp.json


def test_list_users(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    user2 = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})

    user1['is_active'] = True
    user2['is_active'] = True

    resp = client.get('/users/')
    assert resp.json == {'0': user1, '1': user2}


def test_delete_user(client):
    user = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    client.post('/users/', json={'user': user})

    resp = client.delete('/user/0')
    assert resp.status_code == 204

    resp = client.get('/user/0')
    assert resp.status_code == 404


def test_delete_nonexistent_user(client):
    resp = client.delete('/user/9')
    assert resp.status_code == 400


def test_search_user(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    user2 = {'name': "Ivan", 'surname': "Dovgoborodko", 'email': "vania@mail.com"}
    user3 = {'name': "Ivan", 'surname': "Langobard", 'email': "vania2@mail.com"}

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})
    client.post('/users/', json={'user': user3})

    resp = client.get('search/name/Ivan')

    user1['is_active'] = True
    user2['is_active'] = True
    user3['is_active'] = True

    expected_users = [user2, user3]
    assert resp.json == expected_users
