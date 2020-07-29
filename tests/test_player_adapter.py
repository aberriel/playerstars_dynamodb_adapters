from datetime import datetime
from unittest.mock import patch, MagicMock
from playerstars_adapters import PlayerAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)
from playerstars_domain import \
    Player, User, Console, PlayerConsoles, GamePoints


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
            "console_id": "123",
            "game_points": [{
                "game_id": '321',
                "victories": 100
            }]
        }
    ],
    "star_transactions": [],
    "entity_id": "25f86cd2-713e-4aff-8482-82b8fa606423",
    "user":
    {
        "date_birth": "1986-12-16",
        "country": "Brasil",
        "street": 'Avenida Brasil',
        "street_number": '500',
        "street_complement": 'apt 607',
        "neighborhood": 'pechinchão',
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
    "red_star_balance": 321,
    "countries_regions": ["bff41488-bef6-49f6-a258-f1ebff93be78",
                          "4d865d83-46ae-4132-88c4-aa4f67270383"],
    "states_regions": ["02ee1fb8-ad13-4c29-b06c-bbecabf72465",
                       "487ccfaa-da06-43a5-96d8-d7a186081ab8"],
    "favorites": [],
    "points": 30,
    "terms": True
}


def make_mock_player_table():
    table_mock = MagicMock()
    return table_mock


def player_dict_expected(player_id):
    return {
        "consoles":
        [
            {
                "console_id": "123",
                "tag_name": "lol",
                "game_points": [{
                    "game_id": '321',
                    "victories": 100
                }]
            }
        ],
        "entity_id": player_id,
        "user":
        {
            "date_birth": "1987-02-01",
            "country": "Brasil",
            "street": 'Avenida Brasil',
            "street_number": '500',
            "street_complement": 'apt 607',
            "neighborhood": 'pechinchão',
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
        "red_star_balance": 321,
        "favorites": [],
        "countries_regions": [],
        "states_regions": [],
        "star_reservations": [],
        "star_transactions": [],
        "points": 30,
        "purchases": [],
        "terms": False,
        "is_blocked": False,
        "is_admin": False
    }


user1 = User(
    name='Pablinho',
    email='menoti@hotmail.com',
    date_birth=datetime(1987, 2, 1),
    street='Avenida Brasil',
    street_number='500',
    street_complement='apt 607',
    neighborhood='pechinchão',
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
        consoles=[PlayerConsoles(
            console_id='123',
            tag_name='lol',
            game_points=[GamePoints("321", 100)])],
        favorites=[],
        red_star_balance=321,
        golden_star_balance=123,
        points=30
    )
    entity.set_adapter(adapter)
    saved_id = entity.save()
    assert saved_id
    assert entity.to_json()['user']['date_birth']
    assert entity.to_json() == player_dict_expected(saved_id)
