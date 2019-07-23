#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_adapters import BasicDynamodbAdapter
from playerstars_domain import User


class UserAdapter(BasicDynamodbAdapter):
    __table_name__ = 'User'

    def __init__(self):
        super(UserAdapter, self).__init__(self.__table_name__, User)
