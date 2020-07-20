from unittest.mock import patch

from playerstars_domain import TeamTournament

from playerstars_adapters import TeamTournamentAdapter


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_championship_adapter(mock_init):
    TeamTournamentAdapter('team-tournament')

    mock_init.assert_called_with(table_name='team-tournament',
                                 db_endpoint=None,
                                 adapted_class=TeamTournament)
