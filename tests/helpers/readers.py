# -*- coding: utf-8 -*-
import pytest


# Fixtures.


def _sources():
    import django.core.management
    import django_project.models
    import django_project.repositories

    class Django:
        models = django_project.models
        repositories = django_project.repositories

        @staticmethod
        def setup():
            django.core.management.call_command("loaddata", "examples.yaml")

    yield Django


@pytest.fixture(params=_sources())
def m(request):
    """Parametrized fixture with all possible data sources."""
    request.param.setup()
    return request.param.models


@pytest.fixture(params=_sources())
def r(request):
    """Parametrized fixture with all possible repositories."""
    return request.param.repositories
