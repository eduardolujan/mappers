# -*- coding: utf-8 -*-
from operator import methodcaller

from _mappers.mapper import _Converter


def _factory(fields, entity_factory, mapping):
    return _Query()


class _Query(object):
    converters = {
        _Converter.entity: methodcaller("fetchone"),
        _Converter.optional: lambda x: x,
        _Converter.sequence: methodcaller("fetchall"),
    }

    def __call__(self, engine_result):
        return engine_result
