from unittest.mock import patch
from playerstars_adapters import CountryRegionAdapter, StateRegionAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_country_region_adapter(mock1, mock2, mock3):
    adapter = CountryRegionAdapter('CountryRegion', 'localhost-db')
    assert adapter


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_state_region_adapter(mock1, mock2, mock3):
    adapter = StateRegionAdapter('Stateregion', 'localhost-db')
    assert adapter
