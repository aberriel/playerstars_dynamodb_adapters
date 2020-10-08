from clapy_dynamodb_adapter.basic_dynamodb_adapter import BasicDynamodbAdapter
from playerstars_domain import StateRegion


class StateRegionAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(StateRegionAdapter, self).__init__(
            table_name=table_name,
            db_endpoint=db_endpoint,
            adapted_class=StateRegion)
