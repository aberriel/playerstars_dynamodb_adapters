from unittest.mock import MagicMock

from playerstars_adapters.basic_adapter import BasicDynamodbAdapter
from playerstars_domain import BasicEntity


class Entity(BasicEntity):
    def __init__(self, entity_id, nome):
        super(Entity, self).__init__(entity_id)
        self.nome = nome

    def to_json(self):
        return dict(entity_id=self.entity_id,
                    nome=self.nome)

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)


class Adapter(BasicDynamodbAdapter):
    def __init__(self, table_name):
        super(Adapter, self).__init__(table_name, Entity)


def make_mock_client():
    return MagicMock(
        list_tables=MagicMock(
            return_value=dict(TableNames=['tbl1', 'tbl2'])))


def make_mock_table():
    def mock_get_item(**kwargs):
        if kwargs['Key']['entity_id'] == 'id1':
            return dict(Item=dict(entity_id='id1', nome='nome1'))
        else:
            return dict()

    json_data1 = dict(entity_id='id1', nome='nome1')
    json_data2 = dict(entity_id='id2', nome='nome2')

    mock_scan = MagicMock(return_value=dict(Items=[json_data1,
                                                   json_data2]))
    mock_update_item = MagicMock(
        return_value=dict(Item=dict(entity_id='id1', nome='nome4')))
    table_mock = MagicMock(scan=mock_scan,
                           get_item=mock_get_item,
                           update_item=mock_update_item)

    return table_mock


def make_mock_table_with_update_error():
    json_data1 = dict(entity_id='id1', nome='nome1')
    json_data2 = dict(entity_id='id2', nome='nome2')

    mock_scan = MagicMock(return_value=dict(Items=[json_data1,
                                                   json_data2]))
    mock_update_item = MagicMock()
    table_mock = MagicMock(scan=mock_scan,
                           update_item=mock_update_item)

    return table_mock
