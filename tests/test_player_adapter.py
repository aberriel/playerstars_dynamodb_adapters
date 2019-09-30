from datetime import datetime
from unittest.mock import patch, MagicMock
from playerstars_adapters import PlayerAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)
from playerstars_domain import Player, User, Console


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_player_adapter(mock1, mock2, mock3):
    adapter = PlayerAdapter('player', 'localhost-db')
    assert adapter


player_dict_from_db = {
    "consoles":
    [
        {
            "name": "PS 4",
            "entity_id": "1",
            "logo_path": "/images/ps4.png",
            "tag_name": "007"
        },
        {
            "name": "Xbox",
            "entity_id": "11",
            "logo_path": "/images/xbox.png",
            "tag_name": "mario"
        }
    ],
    "star_transactions": [],
    "entity_id": "25f86cd2-713e-4aff-8482-82b8fa606423",
    "user":
    {
        "date_birth": "1986-12-16",
        "country": "Brasil",
        "address": "Rua Jose de Figueiredo 192, Blocos 29, 30 - "
                   "Barra da Tijuca",
        "city": "Rio de Janeiro",
        "nickname": "anselmo.lira",
        "cpf": "123.456.789-00",
        "name": "Anselmo Lira",
        "phone_number": "(21) 99663-6963",
        "state": "Rio de Janeiro",
        "postal_code": "22333-000",
        "email": "playerstars@playerstars.com.br"
    },
    "player_status": "OFFLINE",
    "golden_star_balance": 123,
    "blue_star_balance": 321
}


def make_mock_player_table():
    def mock_get_player(**kwargs):
        if kwargs['Key']['entity_id'] == 'id1':
            return dict(Item=player_dict_from_db)

    table_mock = MagicMock(get_item=mock_get_player)
    return table_mock


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_player_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_player_get(mock, mock1, mock2):
    adapter = PlayerAdapter('player', 'localhost-db')
    result = adapter.get_by_id('id1')
    assert isinstance(result, Player)
    assert result.entity_id == "25f86cd2-713e-4aff-8482-82b8fa606423"


def player_dict_expected(player_id):
    return {
        "consoles":
        [
            {
                "name": "Atari",
                "entity_id": "123",
                "logo_path": "teste/img.png",
                "tag_name": "nick#1",
                "games": []
            }
        ],
        "entity_id": player_id,
        "user":
        {
            "date_birth": "1987-02-01T00:00:00",
            "country": "Brasil",
            "address": "Rua Jose de Figueiredo 192, Blocos 29, 30 - "
                       "Barra da Tijuca",
            "city": "Rio de Janeiro",
            "nickname": "zyzukab",
            "cpf": "123.456.789-01",
            "name": "Pablinho",
            "phone_number": "5555-4321",
            "state": "Rio de Janeiro",
            "postal_code": "90210",
            "email": "menoti@hotmail.com",
            "profile_image": None
        },
        "player_status": "OFFLINE",
        "golden_star_balance": 123,
        "blue_star_balance": 321,
        "favorites": [],
        "countries_regions": [],
        "states_regions": [],
        "star_transactions": [],
        "points": 0,
        "purchases": []
    }


user1 = User(
    name='Pablinho',
    email='menoti@hotmail.com',
    date_birth=datetime(1987, 2, 1),
    address='Rua Jose de Figueiredo 192, Blocos 29, 30 - Barra da Tijuca',
    city='Rio de Janeiro',
    state='Rio de Janeiro',
    country='Brasil',
    postal_code='90210',
    phone_number='5555-4321',
    nickname='zyzukab',
    cpf='123.456.789-01'
)
console1 = Console(
    entity_id='123',
    name='Atari',
    games=[],
    logo_path='teste/img.png',
    tag_name='nick#1'
)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_player_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_player_save(mock, mock1, mock2):
    adapter = PlayerAdapter('player', 'localhost-db')
    entity = Player(
        user=user1,
        consoles=[console1],
        favorites=[],
        blue_star_balance=321,
        golden_star_balance=123
    )
    entity.set_adapter(adapter)
    saved_id = entity.save()
    assert saved_id
    assert entity.to_json()['user']['date_birth']
    assert entity.to_json() == player_dict_expected(saved_id)
