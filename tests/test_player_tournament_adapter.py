from unittest.mock import patch

from playerstars_domain import PlayerTournament

from playerstars_adapters import PlayerTournamentAdapter


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_championship_adapter(mock_init):
    PlayerTournamentAdapter('player-tournament')

    mock_init.assert_called_with(table_name='player-tournament',
                                 db_endpoint=None,
                                 adapted_class=PlayerTournament)
