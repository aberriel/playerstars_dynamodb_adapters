#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import CountryRegion


class CountryRegionAdapter(BasicDynamodbAdapter):
    __table_name__ = 'RegionCountry'

    def __init__(self):
        super(CountryRegionAdapter, self).__init__(self.__table_name__,
                                                   CountryRegion)
