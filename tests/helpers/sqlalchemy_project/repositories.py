# -*- coding: utf-8 -*-
from functools import partial

from sqlalchemy.sql import select

from sqlalchemy_project.tables import DeliveryTable
from sqlalchemy_project.tables import engine
from sqlalchemy_project.tables import GroupTable
from sqlalchemy_project.tables import MessageTable
from sqlalchemy_project.tables import UserTable


def get(name, mapper, *args):
    """Define reader function."""
    return globals()["_get_" + name](mapper, *args)


def _get_load_users(mapper):
    class Users(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load(self):
            query = select([UserTable])
            return self.connection.execute(query)

    return partial(Users.load, Users())


def _get_load_user(mapper):
    class User(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.entity
        def load(self, primary_key):
            query = select([UserTable]).where(UserTable.c.id == primary_key)
            return self.connection.execute(query)

    return partial(User.load, User())


def _get_load_user_or_none(mapper):
    class User(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.optional
        def load(self, primary_key):
            query = select([UserTable]).where(UserTable.c.id == primary_key)
            return self.connection.execute(query)

    return partial(User.load, User())


def _get_load_messages(mapper):
    class Messages(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load(self):
            query = select([MessageTable])
            return self.connection.execute(query)

    return partial(Messages.load, Messages())


def _get_load_total_messages(mapper, field_name):
    class Messages(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load(self):
            # TODO: Count user_id as field_name.
            query = select([MessageTable])
            return self.connection.execute(query)

    return partial(Messages.load, Messages())


def _get_load_deliveries(mapper):
    class Deliveries(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load(self):
            query = select([DeliveryTable])
            return self.connection.execute(query)

    return partial(Deliveries.load, Deliveries())


def _get_load_groups(mapper):
    class Groups(object):
        def __init__(self):
            self.connection = engine.connect()

        @mapper.reader.sequence
        def load(self):
            query = select([GroupTable])
            return self.connection.execute(query)

    return partial(Groups.load, Groups())
