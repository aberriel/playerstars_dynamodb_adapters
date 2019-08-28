from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import CountryRegion


class CountryRegionAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(CountryRegionAdapter, self).__init__(table_name,
                                                   CountryRegion)
