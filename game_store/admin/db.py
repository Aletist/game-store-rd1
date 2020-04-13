from .models import *


def create_db():

    return {
        'users': Users(),
        'user-roles': UserRoles(),
        'roles': Roles(),
        'role-perms': RolePermissions(),
        'perms': Permissions(),
        'resources': Resources()
    }
