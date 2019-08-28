from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import PurchaseHistory


class PurchaseHistoryAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(PurchaseHistoryAdapter, self).__init__(table_name,
                                                     PurchaseHistory)
