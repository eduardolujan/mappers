# -*- coding: utf-8 -*-
import pytest

import helpers


# Fixtures.


@helpers.is_not_empty
def _sources():
    try:
        import django_project.fixtures
        import django_project.models
        import django_project.repositories

        class Django(object):
            tables = django_project.models
            repositories = django_project.repositories

            @staticmethod
            def setup():
                django_project.fixtures.setup()

        yield Django
    except ImportError:
        pass

    try:
        import sqlalchemy_project.fixtures
        import sqlalchemy_project.tables
        import sqlalchemy_project.repositories

        class SQLAlchemy(object):
            tables = sqlalchemy_project.tables
            repositories = sqlalchemy_project.repositories

            @staticmethod
            def setup():
                sqlalchemy_project.fixtures.setup()

        yield SQLAlchemy
    except ImportError:
        pass


@pytest.fixture(params=_sources())
def t(request):
    """Parametrized fixture with all possible data sources."""
    request.param.setup()
    return request.param.tables


@pytest.fixture(params=_sources())
def r(request):
    """Parametrized fixture with all possible repositories."""
    return request.param.repositories
