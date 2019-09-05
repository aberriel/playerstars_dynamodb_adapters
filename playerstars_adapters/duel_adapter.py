from playerstars_domain import Duel
from playerstars_adapters import BasicDynamodbAdapter


class DuelAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(DuelAdapter, self).__init__(table_name, db_endpoint, Duel)
