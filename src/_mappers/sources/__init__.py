# -*- coding: utf-8 -*-
from _mappers.exceptions import MapperError
from _mappers.sources import django
from _mappers.sources import sqlalchemy


def _data_source_factory(data_source):
    if django._is_django_model(data_source):
        schema = django._get_schema(data_source)
        return schema, django._factory
    elif sqlalchemy._is_sqlalchemy_table(data_source):
        schema = sqlalchemy._get_schema(data_source)
        return schema, sqlalchemy._factory
    else:
        raise MapperError
