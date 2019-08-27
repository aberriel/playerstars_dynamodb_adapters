#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import PurchaseHistory


class PurchaseHistoryAdapter(BasicDynamodbAdapter):
    __table_name__ = 'PurchaseHistory'

    def __init__(self):
        super(PurchaseHistoryAdapter, self)\
            .__init__(self.__table_name__, PurchaseHistory)
