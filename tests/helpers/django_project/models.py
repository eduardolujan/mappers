# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


iterable_class = models.QuerySet


class UserModel(models.Model):
    """User table."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    about = models.TextField()
    avatar = models.FileField()

    # Validation rules should handle the generic foreign key field as
    # well.  For example, the nullable check should skip this field,
    # since it does not have the `null` attribute.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")


class GroupModel(models.Model):
    """Group table."""

    name = models.CharField(max_length=255, null=True)


class ChatModel(models.Model):
    """Chat table."""

    name = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(
        "UserModel", related_name="chats", through="ChatSubscriptionModel"
    )


class ChatSubscriptionModel(models.Model):
    """Chat subscription table."""

    user = models.ForeignKey(
        "UserModel", related_name="chat_subscriptions", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        "ChatModel", related_name="chat_subscriptions", on_delete=models.CASCADE
    )


class MessageModel(models.Model):
    """Message table."""

    user = models.ForeignKey(
        "UserModel", related_name="messages", on_delete=models.CASCADE
    )
    text = models.TextField()


class MessageDeliveryModel(models.Model):
    """Message delivery domain model."""

    message = models.ForeignKey(
        "MessageModel", related_name="deliveries", on_delete=models.CASCADE,
    )
    service = models.CharField(max_length=100)
