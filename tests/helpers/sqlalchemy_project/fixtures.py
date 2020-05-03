# -*- coding: utf-8 -*-
from sqlalchemy_project.tables import engine
from sqlalchemy_project.tables import metadata


def setup():
    metadata.create_all(engine)
