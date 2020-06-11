# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


iterable_class = models.QuerySet


class ProfileTable(models.Model):
    """Profile table."""

    login = models.CharField(max_length=255)


class UserTable(models.Model):
    """User table."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    about = models.TextField()
    avatar = models.FileField()
    profile = models.OneToOneField("ProfileTable", on_delete=models.CASCADE)

    # Validation rules should handle the generic foreign key field as
    # well.  For example, the nullable check should skip this field,
    # since it does not have the `null` attribute.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")


class GroupTable(models.Model):
    """Group table."""

    name = models.CharField(max_length=255, null=True)


class ChatTable(models.Model):
    """Chat table."""

    name = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(
        "UserTable", related_name="chats", through="SubscriptionTable"
    )


class SubscriptionTable(models.Model):
    """Chat subscription table."""

    user = models.ForeignKey(
        "UserTable", related_name="subscriptions", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        "ChatTable", related_name="subscriptions", on_delete=models.CASCADE
    )

    class Meta(object):
        """Table settings."""

        unique_together = ("user", "chat")


class MessageTable(models.Model):
    """Message table."""

    user = models.ForeignKey(
        "UserTable", related_name="messages", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        "ChatTable", related_name="messages", on_delete=models.CASCADE
    )
    text = models.TextField()


class DeliveryTable(models.Model):
    """Message delivery table."""

    message = models.ForeignKey(
        "MessageTable", related_name="deliveries", on_delete=models.CASCADE
    )
    service = models.CharField(max_length=100)
