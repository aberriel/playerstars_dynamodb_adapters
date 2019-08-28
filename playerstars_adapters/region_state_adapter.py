#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import StateRegion


class StateRegionAdapter(BasicDynamodbAdapter):
    __table_name__ = 'RegionState'

    def __init__(self):
        super(StateRegionAdapter, self).__init__(self.__table_name__,
                                                 StateRegion)
