from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import PreDuel


class PreDuelAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(PreDuelAdapter, self).__init__(
            table_name, db_endpoint, PreDuel)
