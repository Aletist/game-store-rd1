from abc import ABCMeta, abstractmethod


class SelectItem:

    def __init__(self, storage, field_name):
        self._storage = storage
        self._field_name = field_name

    def query(self, pred):
        return {key:value
                for (key, value) in self._storage.items()
                if self._field_name in value
                and pred(value[self._field_name])}

    def fetchone(self, pred):
        for item in self.query(pred=pred).values():
            return item

    def fetchall(self, pred):
        return self.query(pred=pred).values()


class BaseModel(metaclass=ABCMeta):

    @property
    @abstractmethod
    def storage(self):
        pass

    @property
    @abstractmethod
    def fields(self):
        pass

    @property
    @abstractmethod
    def primary_field_name(self):
        pass

    def __init__(self):
        self._primary_key = 0

    def __getattr__(self, item):
        if item in self.fields:
            return SelectItem(storage=self.storage, field_name=item)

        return self.__getattribute__(item)

    def insert(self, data):
        data.update({self.primary_field_name: self._primary_key})

        self.storage[self._primary_key] = data
        self._primary_key += 1

    def get_by_id(self, primary_key):
        return self.storage[primary_key]


class Users(BaseModel):
    _fields = {'name', 'surname', 'email', 'is_active', 'password', 'username'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'user_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class UserRoles(BaseModel):

    _fields = {'user', 'role'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'user-role_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class Roles(BaseModel):

    _fields = {'name'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'role_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class RolePermissions(BaseModel):

    _fields = {'role', 'perm'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'role-permission_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class Permissions(BaseModel):
    _fields = {'resource', 'action'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'permission_id'

    def __init__(self):
        super().__init__()
        self._storage = {}


class Resources(BaseModel):

    _fields = {'name'}

    @property
    def storage(self):
        return self._storage

    @property
    def fields(self):
        return self._fields

    @property
    def primary_field_name(self):
        return 'resource_id'

    def __init__(self):
        super().__init__()
        self._storage = {}