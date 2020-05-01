# -*- coding: utf-8 -*-
from datetime import date

from django_project.models import ChatModel
from django_project.models import GroupModel
from django_project.models import MessageDeliveryModel
from django_project.models import MessageModel
from django_project.models import UserModel


def setup():
    """Load data."""
    UserModel.objects.create(
        pk=1,
        created=date(2019, 1, 1),
        modified=date(2019, 1, 1),
        name="",
        about="",
        avatar="",
    )
    UserModel.objects.create(
        pk=2,
        created=date(2019, 1, 1),
        modified=date(2019, 1, 1),
        name="",
        about="",
        avatar="",
    )
    GroupModel.objects.create(pk=1, name=None)
    GroupModel.objects.create(pk=2, name="")
    ChatModel.objects.create(pk=1, name="")
    ChatModel.objects.create(pk=2, name="")
    MessageModel.objects.create(pk=1, user_id=1, text="")
    MessageModel.objects.create(pk=2, user_id=2, text="")
    MessageDeliveryModel.objects.create(pk=1, message_id=1, service="")
    MessageDeliveryModel.objects.create(pk=2, message_id=2, service="")
