# -*- coding: utf-8 -*-
from _mappers.exceptions import MapperError
from _mappers.sources import django


def _data_source_factory(data_source):
    if django._is_django_model(data_source):
        schema = django._get_schema(data_source)
        return schema, django._factory
    else:
        raise MapperError
