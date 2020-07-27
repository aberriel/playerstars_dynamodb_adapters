from clapy_dynamodb_adapter.basic_dynamodb_adapter import BasicDynamodbAdapter
from playerstars_domain import Player


class PlayerAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(PlayerAdapter, self).__init__(table_name, db_endpoint, Player)
