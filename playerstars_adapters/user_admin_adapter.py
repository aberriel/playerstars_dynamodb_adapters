from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import UserAdmin


class UserAdminAdapter(BasicDynamodbAdapter):
    __table_name__ = 'UserAdmin'

    def __init__(self):
        super(UserAdminAdapter, self).__init__(self.__table_name__, UserAdmin)
