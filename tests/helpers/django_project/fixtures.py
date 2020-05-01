# -*- coding: utf-8 -*-
from datetime import date

from django_project.models import ChatTable
from django_project.models import DeliveryTable
from django_project.models import GroupTable
from django_project.models import MessageTable
from django_project.models import ProfileTable
from django_project.models import SubscriptionTable
from django_project.models import UserTable


def setup():
    """Load data."""
    ProfileTable.objects.create(pk=1, login="")
    ProfileTable.objects.create(pk=2, login="")
    UserTable.objects.create(
        pk=1,
        created=date(2019, 1, 1),
        modified=date(2019, 1, 1),
        name="",
        about="",
        avatar="",
        profile_id=1,
    )
    UserTable.objects.create(
        pk=2,
        created=date(2019, 1, 1),
        modified=date(2019, 1, 1),
        name="",
        about="",
        avatar="",
        profile_id=2,
    )
    GroupTable.objects.create(pk=1, name=None)
    GroupTable.objects.create(pk=2, name="")
    ChatTable.objects.create(pk=1, name="")
    ChatTable.objects.create(pk=2, name="")
    SubscriptionTable.objects.create(pk=1, user_id=1, chat_id=1)
    SubscriptionTable.objects.create(pk=2, user_id=2, chat_id=2)
    MessageTable.objects.create(pk=1, user_id=1, chat_id=1, text="")
    MessageTable.objects.create(pk=2, user_id=2, chat_id=2, text="")
    DeliveryTable.objects.create(pk=1, message_id=1, service="")
    DeliveryTable.objects.create(pk=2, message_id=2, service="")
