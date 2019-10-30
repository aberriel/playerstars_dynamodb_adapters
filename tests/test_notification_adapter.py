from unittest.mock import patch
from playerstars_adapters import NotificationAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_duel_adapter(mock1, mock2, mock3):
    adapter = NotificationAdapter('duel', 'localhost-db')
    assert adapter
