from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Player


class PlayerAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Player'

    def __init__(self):
        super(PlayerAdapter, self).__init__(self.__table_name__, Player)
