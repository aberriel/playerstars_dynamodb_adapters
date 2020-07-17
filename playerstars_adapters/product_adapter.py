from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Product


class ProductAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(ProductAdapter, self).__init__(
            table_name, db_endpoint, Product)
