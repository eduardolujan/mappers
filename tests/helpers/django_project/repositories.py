# -*- coding: utf-8 -*-
from django.db.models import Count

from django_project import models


def get(name, mapper, *args):
    """Define reader function."""
    return globals()["_get_" + name](mapper, *args)


def _get_load_users(mapper, user):
    @mapper.reader.sequence
    def load_users():
        return models.UserModel.objects.all()

    return load_users


def _get_load_user(mapper, user, user_id):
    @mapper.reader.entity
    def load_user(primary_key):
        return models.UserModel.objects.filter(pk=primary_key)

    return load_user


def _get_load_user_or_none(mapper, user, user_id):
    @mapper.reader.optional
    def load_user(primary_key):
        return models.UserModel.objects.filter(pk=primary_key)

    return load_user


def _get_load_messages(mapper, message):
    @mapper.reader.sequence
    def load_messages():
        return models.MessageModel.objects.all()

    return load_messages


def _get_load_total_messages(mapper, message, field_name):
    @mapper.reader.sequence
    def load_messages():
        q = {field_name: Count("user_id")}
        return models.MessageModel.objects.annotate(**q)

    return load_messages


def _get_load_deliveries(mapper, delivery):
    @mapper.reader.sequence
    def load_deliveries():
        return models.MessageDeliveryModel.objects.all()

    return load_deliveries


def _get_load_groups(mapper, group):
    @mapper.reader.sequence
    def load_groups():
        return models.GroupModel.objects.all()

    return load_groups
