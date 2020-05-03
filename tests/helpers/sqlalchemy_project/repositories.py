# -*- coding: utf-8 -*-
from sqlalchemy.sql import select

from sqlalchemy_project.tables import engine
from sqlalchemy_project.tables import UserTable


def get(name, mapper, *args):
    """Define reader function."""
    return globals()["_get_" + name](mapper, *args)


def _get_load_users(mapper):
    class Users(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load():
            query = select([UserTable])
            return self.connection.execute(query)

    return Users().load
