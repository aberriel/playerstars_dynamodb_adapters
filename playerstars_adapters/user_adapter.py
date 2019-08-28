from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import User


class UserAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(UserAdapter, self).__init__(table_name, User)
