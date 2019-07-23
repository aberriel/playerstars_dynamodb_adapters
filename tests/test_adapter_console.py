#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch, MagicMock
from playerstars_adapters import ConsoleAdapter
from tests.basic_adapter_utils import (
    make_mock_client, Adapter, Entity, make_mock_table,
    make_mock_table_with_update_error)


class Patches:
    BASE = 'playerstars_adapters.basic_adapter'
    BOTO3_CLIENT = f'{BASE}.boto3.client'
    GET_TABLE = f'{BASE}.BasicDynamodbAdapter.get_table'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE)
def test_adapter_console(mock1, mock2):
    adapter = ConsoleAdapter()
    assert adapter
