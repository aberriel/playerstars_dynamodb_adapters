from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Console


class ConsoleAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(ConsoleAdapter, self).__init__(table_name, Console)
