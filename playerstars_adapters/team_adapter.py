from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Team


class TeamAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Team'

    def __init__(self):
        super(TeamAdapter, self).__init__(self.__table_name__, Team)
