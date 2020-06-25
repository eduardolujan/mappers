# -*- coding: utf-8 -*-
from sqlalchemy_project.tables import engine
from sqlalchemy_project.tables import metadata


def setup():
    """Load data."""
    metadata.create_all(engine)
