from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Team


class TeamAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(TeamAdapter, self).__init__(table_name, Team)
