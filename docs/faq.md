# FAQ

## I want to reuse a reader inside another reader

Use private functions for it. It's the best option available. It's not necessary
to copypaste filter logic from one reader to another just to build something
slitely different on top of it.

```python

>>> from dataclasses import dataclass

>>> @dataclass
... class User:
...     primary_key: int
...     name: str

>>> from mappers import Mapper

>>> from django_project.models import UserTable

>>> mapper = Mapper(User, UserTable, {'primary_key': 'id'})

>>> def _load_users():
...     return UserTable.objects.all()

>>> load_users = mapper.reader.sequence(_load_users)

>>> @mapper.reader.entity
... def load_user(primary_key):
...     return _load_users().filter(pk=primary_key)

>>> load_users()  # doctest: +ELLIPSIS
[User(primary_key=1, ...), User(primary_key=2, ...)]

>>> load_user(1)  # doctest: +ELLIPSIS
User(primary_key=1, ...)

```
