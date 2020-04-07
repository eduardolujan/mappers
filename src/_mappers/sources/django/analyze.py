# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect

try:
    from django.db.models import Model as DjangoModel

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_django_model(data_source):
    if IS_AVAILABLE:
        return inspect.isclass(data_source) and issubclass(data_source, DjangoModel)
    else:
        return False


def _get_fields(data_source, exclude=None):
    fields = {}
    for field in data_source._meta._get_fields():
        if field is exclude:
            continue
        names = _get_field_names(field)
        disassembled = _disassemble_field(field)
        for name in names:
            fields[name] = disassembled
    return fields


def _get_field_names(field):
    yield field.name
    attname = getattr(field, "attname", None)
    if attname is not None and field.name != attname:
        yield attname


def _disassemble_field(field):
    is_generic_foreign_key = bool(getattr(field, "get_content_type", None))
    if is_generic_foreign_key:
        disassembled = {
            "is_nullable": False,
            "is_link": False,
            "is_collection": False,
        }
    else:
        disassembled = {
            "is_nullable": bool(field.null),
            "is_link": field.is_relation,
            "is_collection": field.many_to_many,
        }
    if disassembled["is_link"] and not disassembled["is_collection"]:
        disassembled["link"] = field.related_model
        disassembled["link_to"] = _get_fields(
            field.related_model, exclude=field.remote_field
        )
    return disassembled
