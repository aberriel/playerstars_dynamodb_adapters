from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import StateRegion


class StateRegionAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(StateRegionAdapter, self).__init__(table_name, db_endpoint,
                                                 StateRegion)
