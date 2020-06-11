# -*- coding: utf-8 -*-
import pytest

import helpers


# Fixtures.


@helpers.is_not_empty
def _sources():
    import django_project.fixtures
    import django_project.models
    import django_project.repositories

    class Django:
        tables = django_project.models
        repositories = django_project.repositories

        @staticmethod
        def setup():
            django_project.fixtures.setup()

    yield Django


@pytest.fixture(params=_sources())
def t(request):
    """Parametrized fixture with all possible data sources."""
    request.param.setup()
    return request.param.tables


@pytest.fixture(params=_sources())
def r(request):
    """Parametrized fixture with all possible repositories."""
    return request.param.repositories
