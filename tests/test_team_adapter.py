#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
from playerstars_adapters import TeamAdapter
from tests.basic_adapter_utils import (
    make_mock_client, make_mock_table, Patches)


@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_team_adapter(mock1, mock2, mock3):
    adapter = TeamAdapter()
    assert adapter
