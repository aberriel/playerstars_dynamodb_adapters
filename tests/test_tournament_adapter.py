from unittest.mock import patch

from playerstars_domain import Tournament

from playerstars_adapters import TournamentAdapter


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_championship_adapter(mock_init):
    TournamentAdapter('tournament')

    mock_init.assert_called_with(table_name='tournament',
                                 db_endpoint=None,
                                 adapted_class=Tournament)
