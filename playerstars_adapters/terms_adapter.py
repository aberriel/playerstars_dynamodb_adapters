from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Terms


class TermsAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(TermsAdapter, self).__init__(
            table_name, db_endpoint, Terms)
