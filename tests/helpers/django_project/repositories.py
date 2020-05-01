# -*- coding: utf-8 -*-
from django.db.models import Count

from django_project import models


def get(name, mapper, *args):
    """Define reader function."""
    return globals()["_get_" + name](mapper, *args)


def _get_load_users(mapper):
    @mapper.reader.sequence
    def load_users():
        return models.UserTable.objects.all()

    return load_users


def _get_load_user(mapper):
    @mapper.reader.entity
    def load_user(primary_key):
        return models.UserTable.objects.filter(pk=primary_key)

    return load_user


def _get_load_user_or_none(mapper):
    @mapper.reader.optional
    def load_user(primary_key):
        return models.UserTable.objects.filter(pk=primary_key)

    return load_user


def _get_load_messages(mapper):
    @mapper.reader.sequence
    def load_messages():
        return models.MessageTable.objects.all()

    return load_messages


def _get_load_total_messages(mapper, field_name):
    @mapper.reader.sequence
    def load_messages():
        q = {field_name: Count("user_id")}
        return models.MessageTable.objects.annotate(**q)

    return load_messages


def _get_load_deliveries(mapper):
    @mapper.reader.sequence
    def load_deliveries():
        return models.DeliveryTable.objects.all()

    return load_deliveries


def _get_load_groups(mapper):
    @mapper.reader.sequence
    def load_groups():
        return models.GroupTable.objects.all()

    return load_groups
