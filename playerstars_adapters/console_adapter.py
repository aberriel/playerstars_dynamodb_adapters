#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Console


class ConsoleAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Console'

    def __init__(self):
        super(ConsoleAdapter, self).__init__(self.__table_name__, Console)
