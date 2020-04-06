from abc import ABCMeta, abstractmethod


class SelectItem:

    def __init__(self, storage, field_name):
        self._storage = storage
        self._field_name = field_name

    def query(self, pred):

        raise NotImplementedError

    def fetchone(self, pred):

        for item in self.query(pred=pred):
            return item


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
    # todo store password hash instead of raw string
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
