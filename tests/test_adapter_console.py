#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import ConsoleAdapter


def test_adapter_game():
    adapter = ConsoleAdapter()
    assert adapter
