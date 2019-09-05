from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import UserAdmin


class UserAdminAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(UserAdminAdapter, self).__init__(
            table_name, db_endpoint, UserAdmin)
