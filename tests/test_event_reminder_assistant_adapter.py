from unittest.mock import patch

from playerstars_domain.event_reminder_assistant import EventReminderAssistant

from playerstars_adapters.event_reminder_assistant_adapter import \
    EventReminderAssistantAdapter


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_era_adapter(mock_init):
    adapter = EventReminderAssistantAdapter(table_name='era_table')

    mock_init.assert_called_with(table_name='era_table',
                                 db_endpoint=None,
                                 adapted_class=EventReminderAssistant)
    assert isinstance(adapter, EventReminderAssistantAdapter)
