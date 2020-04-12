from .models import *


def create_db():

    return {
        'users': Users(),
        'user-roles': UserRoles(),
        'roles': Roles(),
        'role-permissions': RolePermissions(),
        'permissions': Permissions(),
        'resources': Resources()
    }
