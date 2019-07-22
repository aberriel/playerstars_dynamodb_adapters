#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter


class ConsoleAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Console'

    def __init__(self):
        super(ConsoleAdapter, self).__init__(self.__table_name__, ConsoleAdapter)
