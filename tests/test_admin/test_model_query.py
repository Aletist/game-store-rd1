def test_select_by_email(users_db):

    user = users_db.email.fetchone(lambda x: x.startswith('lesya'))
    assert user['surname'] == 'Ukrainka'
