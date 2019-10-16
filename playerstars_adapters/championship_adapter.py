from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Championship


class ChampionshipAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(ChampionshipAdapter, self).__init__(table_name,
                                                  db_endpoint,
                                                  Championship)
