from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import ConvertStarRate


class ConvertStarRateAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(ConvertStarRateAdapter, self).__init__(
            table_name, db_endpoint, ConvertStarRate)
