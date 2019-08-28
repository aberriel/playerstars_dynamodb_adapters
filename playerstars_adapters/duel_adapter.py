from playerstars_domain import Duel
from playerstars_adapters import BasicDynamodbAdapter


class DuelAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(DuelAdapter, self).__init__(table_name, Duel)
