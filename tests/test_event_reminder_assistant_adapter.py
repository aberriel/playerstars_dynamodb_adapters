from unittest.mock import patch, MagicMock
from playerstars_adapters import EventReminderAssistantAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)
from playerstars_domain import EventReminderAssistant


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('playerstars_adapters.event.reminder.assistant.BasicDynamodbAdapter')
def test_era_adapter(mock1, mock2, mock3):
    adapter = EventReminderAssistantAdapter('player', 'localhost-db')
    assert adapter
    assert isinstance(adapter, EventReminderAssistantAdapter)
