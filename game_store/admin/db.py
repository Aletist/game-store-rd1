from . import models


def create_db():

    return {
        'users': models.Users(),
        'user-roles': models.UserRoles(),
        'roles': models.Roles(),
        'role-perms': models.RolePermissions(),
        'perms': models.Permissions(),
        'resources': models.Resources()
    }
