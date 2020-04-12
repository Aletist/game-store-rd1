# from pytest import fixture
#
# from game_store.admin.models import Users
#
#
# @fixture()
# def user_data():
#     return [{
#         'name': 'Taras',
#         'surname': 'Shevchenko',
#         'email': 'taras@shevchenko.name',
#         'password': 'Zapovit2.0'
#     }, {
#         'name': 'Ivan',
#         'surname': 'Franko',
#         'email': 'ivan@franko.name',
#         'password': 'Kamenyar123'
#     }, {
#         'name': 'Lesya',
#         'surname': 'Ukrainka',
#         'email': 'lesya@ukrainka.name',
#         'password': 'Mavka789'
#     }]
#
# @fixture()
# def users_db(user_data):
#
#     users = Users()
#     for u in user_data:
#         users.insert(u)
#     return users
#
#
# def test_select_by_email(users_db):
#
#     user = users_db.email.fetchone(lambda x: x.startswith('lesya'))
#     print(user)
#     assert user['surname'] == 'Ukrainka'
