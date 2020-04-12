from flask import abort


# current_app.auth_checker.check('Users', 'read', g.user['user_id'])
class AuthChecker:

    def __init__(self, db):
        self._db = db

    def check(self, resource, action, user_id):
        abort(403)
