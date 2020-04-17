from flask import abort


class AuthChecker:

    def __init__(self, db):
        self._db = db

    def check(self, resource, action, user_id):
        try:
            roles = [item['role']
                     for item
                     in self._db['user-roles'].user.fetchall(lambda x:
                                                             x == user_id)]
            permissions = [item['perm']
                           for item
                           in self._db['role-perms'].role.fetchall(lambda x:
                                                                   x in roles)]
            resource = self._db['resources'].name.fetchone(lambda x:
                                                           x == resource
                                                           )['resource_id']
            has_rights = False

            for permission in permissions:
                perm = self._db['perms'].get_by_id(permission)
                if perm['action'] == action \
                        and perm['resource'] == resource:
                    has_rights = True
                    break

            if not has_rights:
                abort(403)

        except TypeError:
            abort(403)
