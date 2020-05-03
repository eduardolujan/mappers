# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from sqlalchemy import Table

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_sqlalchemy_table(data_source):
    if IS_AVAILABLE:
        return isinstance(data_source, Table)
    else:
        return False


def _get_schema(data_source):
    schema = {}
    _get_fields(data_source, schema)
    return schema


def _get_fields(data_source, schema):
    schema[data_source] = fields = {}
    for field in data_source.columns:
        disassembled = _disassemble_field(field)
        fields[field.name] = disassembled


def _disassemble_field(field):
    disassembled = {
        "is_nullable": field.nullable,
        "is_link": None,
        "is_collection": None,
    }
    return disassembled
