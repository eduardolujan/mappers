# -*- coding: utf-8 -*-
import pytest


# Fixtures.


def _readers():
    try:
        import readers.annotations

        yield readers.annotations
    except (SyntaxError, ImportError):
        pass

    import readers.arguments

    yield readers.arguments


@pytest.fixture(params=_readers())
def r(request):
    """Parametrized fixture with all possible reader definitions."""
    return request.param
