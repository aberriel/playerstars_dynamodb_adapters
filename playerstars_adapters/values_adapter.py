from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Values


class ValuesAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(ValuesAdapter, self).__init__(
            table_name, db_endpoint, Values)
