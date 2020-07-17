from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import CountryRegion


class CountryRegionAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(CountryRegionAdapter, self).__init__(table_name, db_endpoint,
                                                   CountryRegion)
