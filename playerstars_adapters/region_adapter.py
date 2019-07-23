#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import Region


class RegionAdapter(BasicDynamodbAdapter):
    __table_name__ = 'Region'

    def __init__(self):
        super(RegionAdapter, self).__init__(self.__table_name__, Region)
