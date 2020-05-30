# Mappers

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/mappers/1?style=flat-square)](https://dev.azure.com/proofit404/mappers/_build/latest?definitionId=1&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/mappers/1?style=flat-square)](https://dev.azure.com/proofit404/mappers/_build/latest?definitionId=1&branchName=master)
[![pypi](https://img.shields.io/pypi/v/mappers?style=flat-square)](https://pypi.python.org/pypi/mappers/)

Declarative mappers to domain entities

## One to one mapping

### Define an entity with dataclass

```pycon

>>> from dataclasses import dataclass
>>> from datetime import datetime
>>> from typing import NewType

>>> UserId = NewType("UserId", int)

>>> @dataclass
... class User:
...     primary_key: UserId
...     created: datetime
...     modified: datetime
...     name: str
...     about: str
...     avatar: str

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class UserTable(models.Model):
...     created = models.DateTimeField(auto_now_add=True)
...     modified = models.DateTimeField(auto_now=True)
...     name = models.CharField(max_length=255)
...     about = models.TextField()
...     avatar = models.FileField()
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from mappers import Mapper

>>> from django_project.models import UserTable

>>> mapper = Mapper(User, UserTable, {"primary_key": "id"})

>>> @mapper.reader.sequence
... def load_users():
...     """Load all users from the database."""
...     return UserTable.objects.all()

```

### Read list of domain entities directly from data source

```pycon

>>> load_users()  # doctest: +ELLIPSIS
[User(primary_key=1, created=datetime.datetime(...), modified=datetime.datetime(...), name='', about='', avatar=''), ...]

```

## Mapping evaluated field

### Define an entity with dataclass

```pycon

>>> from dataclasses import dataclass
>>> from typing import NewType

>>> ChatId = NewType("ChatId", int)

>>> @dataclass
... class Chat:
...     primary_key: ChatId
...     name: str
...     is_hidden: bool

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class ChatTable(models.Model):
...     name = models.CharField(max_length=255)
...     subscribers = models.ManyToManyField(
...         "UserTable",
...         related_name="chats",
...         through="SubscriptionTable",
...     )
...
...     class Meta:
...         app_label = "app"

>>> class SubscriptionTable(models.Model):
...     user = models.ForeignKey(
...         "UserTable",
...         related_name="chat_subscriptions",
...         on_delete=models.CASCADE,
...     )
...     chat = models.ForeignKey(
...         "ChatTable",
...         related_name="chat_subscriptions",
...         on_delete=models.CASCADE,
...     )
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from django.db import models
>>> from mappers import Mapper, Evaluated

>>> from django_project.models import ChatTable, SubscriptionTable

>>> mapper = Mapper(Chat, ChatTable, {
...     "primary_key": "id",
...     "is_hidden": Evaluated(),
... })

>>> @mapper.reader.sequence
... def load_chats(user: User):
...     """Load all chats from the point of view of the logged-in user."""
...     subscription = SubscriptionTable.objects.filter(
...         user=user.primary_key,
...         chat=models.OuterRef("pk")
...     )
...     chats = ChatTable.objects.annotate(
...         is_hidden=~models.Exists(subscription),
...     )
...     return chats

```

### Read list of domain entities directly from data source

```pycon

>>> load_chats(load_users()[0])  # doctest: +ELLIPSIS
[Chat(primary_key=1, name='', is_hidden=False), ...]

```

## Mapping with nested objects

### Define an entity with an nested entity

```pycon

>>> from dataclasses import dataclass
>>> from typing import NewType

>>> MessageId = NewType("MessageId", int)

>>> @dataclass
... class Message:
...     primary_key: MessageId
...     user: User
...     text: str
...
...     def written_by(self, user: User) -> bool:
...         return self.user.primary_key == user.primary_key

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class MessageTable(models.Model):
...     user = models.ForeignKey(
...         "UserTable",
...         related_name="messages",
...         on_delete=models.CASCADE,
...     )
...     text = models.TextField()
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from mappers import Mapper

>>> from django_project.models import MessageTable

>>> mapper = Mapper(Message, MessageTable, {
...     "primary_key": "id",
...     "user": Mapper({
...         "primary_key": "id",
...     }),
... })

>>> @mapper.reader.sequence
... def load_messages():
...     """Load list of all messages."""
...     return MessageTable.objects.all()

```

### Read list of domain entities directly from data source

```pycon

>>> messages = load_messages()

>>> messages  # doctest: +ELLIPSIS
[Message(primary_key=1, user=User(primary_key=1, ...), text=''), ...]

>>> messages[0].written_by(load_users()[0])
True

>>> messages[1].written_by(load_users()[0])
False

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The mappers library is part of the SOLID python family.</i></p>
