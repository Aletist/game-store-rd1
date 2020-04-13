from flask import abort


class AuthChecker:

    def __init__(self, db):
        self._db = db

    # todo: refactor this and catch only the specified exceptions.
    def check(self, resource, action, user_id):
        try:
            role_ids = [item['role']
                     for item
                     in self._db['user-roles']
                         .user.fetchall(lambda x: x == user_id)]
            perm_ids = [item['perm']
                     for item
                     in self._db['role-perms']
                         .role.fetchall(lambda x: x in role_ids)]
            resource_id = self._db['resources'].name.fetchone(lambda x: x == resource)['resource_id']
            for id in perm_ids:
                perm = self._db['perms'].get_by_id(id)
                if perm['action'] == action and perm['resource'] == resource_id:
                    return True
        except BaseException:
            abort(403)
