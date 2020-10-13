from botocore.exceptions import ClientError
from unittest.mock import MagicMock


class Patches:
    BASE = 'clapy_dynamodb_adapter.basic_dynamodb_adapter'
    BOTO3_CLIENT = f'{BASE}.boto3.client'
    GET_TABLE = f'{BASE}.BasicDynamodbAdapter.get_table'


def raise_if_empty(arg):
    if isinstance(arg, (list, set)):
        for value in arg:

            raise_if_empty(arg=value)
    elif isinstance(arg, dict):
        for value in arg.values():
            raise_if_empty(arg=value)

    if hasattr(arg, '__len__') and len(arg) == 0:
        raise ValueError('Item vazio encontrado')


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
    mock_delete_item = MagicMock(
        side_effect=ClientError(
            error_response=dict(
                Error=dict(Code=500, Message='oops')),
            operation_name='delete'))
    table_mock = MagicMock(scan=mock_scan,
                           get_item=mock_get_item,
                           update_item=mock_update_item,
                           delete_item=mock_delete_item)

    return table_mock
