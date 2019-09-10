from unittest.mock import patch, MagicMock
from playerstars_adapters import UserAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)
from playerstars_domain import User
from datetime import datetime


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_user_adapter(mock1, mock2, mock3):
    adapter = UserAdapter('User', 'localhost-db')
    assert adapter


def make_mock_player_table():
    table_mock = MagicMock(get_item={})
    return table_mock


def user_dict_expected(user_id):
    return {
        "date_birth": "1987-01-01T00:00:00",
        "country": "Brasil",
        "address": "Rua José de Figueiredo 192, Blocos 29, 30 - "
                   "Barra da Tijuca",
        "city": "Rio de Janeiro",
        "entity_id": user_id,
        "nickname": "zyzukab",
        "cpf": "123.456.789-01",
        "name": "Pablinho",
        "phone_number": "5555-4321",
        "state": "Rio de Janeiro",
        "postal_code": "90210",
        "email": "menoti@hotmail.com",
        "profile_image": None
    }


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_player_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_player_save(mock, mock1, mock2):
    adapter = UserAdapter('User', 'localhost-db')
    entity = User(
        name='Pablinho',
        email='menoti@hotmail.com',
        date_birth=datetime(1987, 1, 1),
        address='Rua José de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca',
        city='Rio de Janeiro',
        state='Rio de Janeiro',
        country='Brasil',
        postal_code='90210',
        phone_number='5555-4321',
        entity_id='1234',
        nickname='zyzukab',
        cpf='123.456.789-01'
    )
    entity.set_adapter(adapter)
    saved_id = entity.save()
    assert saved_id
    assert entity.to_json()['date_birth']
    assert entity.to_json() == user_dict_expected(saved_id)
