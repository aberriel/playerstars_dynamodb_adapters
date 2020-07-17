from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Team


class TeamAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(TeamAdapter, self).__init__(table_name, db_endpoint, Team)
