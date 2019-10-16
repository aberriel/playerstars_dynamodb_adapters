from playerstars_adapters import ChampionshipAdapter
from tests.basic_adapter_utils import (
    make_mock_client,
    make_mock_table,
    Patches
)
from unittest.mock import patch


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_championship_adapter(mock1, mock2, mock3):
    adapter = ChampionshipAdapter('championship', 'localhost-db')
    assert adapter
