from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Notification


class NotificationAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name, db_endpoint):
        super(NotificationAdapter, self).__init__(
            table_name, db_endpoint, Notification)
