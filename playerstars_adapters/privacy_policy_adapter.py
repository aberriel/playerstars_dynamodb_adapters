from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import PrivacyPolicy


class PrivacyPolicyAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint=None):
        super(PrivacyPolicyAdapter, self).__init__(
            table_name, db_endpoint, PrivacyPolicy)
