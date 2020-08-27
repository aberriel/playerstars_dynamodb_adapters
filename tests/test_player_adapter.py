from unittest.mock import patch

from playerstars_domain import Player

from playerstars_adapters import PlayerAdapter


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_era_adapter(mock_init):
    PlayerAdapter(table_name='player_table')

    mock_init.assert_called_with(table_name='player_table',
                                 db_endpoint=None,
                                 adapted_class=Player)
