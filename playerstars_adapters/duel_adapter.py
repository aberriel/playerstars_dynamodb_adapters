from playerstars_domain import Duel
from playerstars_adapters import BasicDynamodbAdapter


class DuelAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Duel'

    def __init__(self):
        super(DuelAdapter, self).__init__(self.__table_name__, Duel)
