from unittest.mock import patch, MagicMock
from playerstars_adapters import UserAdminAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)
from playerstars_domain import UserAdmin


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_user_adapter(mock1, mock2, mock3):
    adapter = UserAdminAdapter('UserAdmin', 'localhost-db')
    assert adapter


def make_mock_player_table():
    table_mock = MagicMock(get_item={})
    return table_mock


def user_dict_expected(user_id):
    return {
        "entity_id": user_id,
        "name": "Pablinho",
        "email": "menoti@hotmail.com"
    }


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_player_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_player_save(mock, mock1, mock2):
    adapter = UserAdminAdapter('UserAdmin', 'localhost-db')
    entity = UserAdmin(
        name='Pablinho',
        email='menoti@hotmail.com',
    )
    entity.set_adapter(adapter)
    saved_id = entity.save()
    assert saved_id
    assert entity.to_json() == user_dict_expected(saved_id)
