# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table


iterable_class = None


engine = create_engine("sqlite:///:memory:")


metadata = MetaData()


ProfileTable = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
)


UserTable = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created", DateTime, default=datetime.now, nullable=False),
    Column(
        "modified",
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    ),
    Column("name", String, nullable=False),
    Column("about", String, nullable=False),
    Column("avatar", String, nullable=False),
    Column("profile_id", None, ForeignKey("profiles.id")),  # TODO: one to one
)


GroupTable = Table(
    "groups", metadata, Column("id", Integer, primary_key=True), Column("name", String)
)


ChatTable = Table(
    "chats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)


SubscriptionTable = Table(
    "subscriptions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", None, ForeignKey("users.id")),
    Column("chat_id", None, ForeignKey("chats.id")),
    # TODO: unique together
)


MessageTable = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", None, ForeignKey("users.id")),
    Column("chat_id", None, ForeignKey("chats.id")),
    Column("text", String, nullable=False),
)


DeliveryTable = Table(
    "deliveries",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message_id", None, ForeignKey("messages.id")),
    Column("service", String, nullable=False),
)
