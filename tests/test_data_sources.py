# -*- coding: utf-8 -*-
"""Tests related to different data sources."""
import pytest

from mappers import Evaluated
from mappers import Mapper


pytestmark = pytest.mark.django_db


def test_reader_representation(e, t, r):
    """Reader representation should show the name of the function."""
    mapper = Mapper(e.User, t.UserTable, {"primary_key": "id"})

    @mapper.reader.entity
    def foo():
        pass  # pragma: no cover

    assert repr(foo) == "<Reader::foo>"

    @mapper.reader.optional
    def bar():
        pass  # pragma: no cover

    assert repr(bar) == "<Reader::bar>"

    @mapper.reader.sequence
    def baz():
        pass  # pragma: no cover

    assert repr(baz) == "<Reader::baz>"

    @mapper.reader.iterable
    def quiz():
        pass  # pragma: no cover

    assert repr(quiz) == "<Reader::quiz>"


# Converters.


def test_result_iterable_converter(e, t, r):
    """Return iterator of entities."""
    mapper = Mapper(e.User, t.UserTable, {"primary_key": "id"})

    iterate_users = r.get("iterate_users", mapper)

    result = iterate_users()

    assert isinstance(result, type(iter([])))

    user1 = next(result)
    user2 = next(result)

    assert isinstance(user1, e.User)
    assert isinstance(user2, e.User)

    with pytest.raises(StopIteration):
        next(result)


def test_result_list_converter(e, t, r):
    """Infer collection converter from the function result annotation.

    This code should return a list of `User` instances.

    """
    mapper = Mapper(e.User, t.UserTable, {"primary_key": "id"})

    load_users = r.get("load_users", mapper)

    result = load_users()

    assert isinstance(result, list)

    user1, user2 = result

    assert isinstance(user1, e.User)
    assert isinstance(user2, e.User)


def test_result_object_converter(e, t, r):
    """Return a single object.

    If instead of converter annotation will be an entity class, we should return a
    single object.  Not a collection.

    """
    mapper = Mapper(e.User, t.UserTable, {"primary_key": "id"})

    load_user = r.get("load_user", mapper)

    user1 = load_user(1)

    assert isinstance(user1, e.User)

    with pytest.raises(t.UserTable.DoesNotExist):
        load_user(3)


def test_result_optional_converter(e, t, r):
    """Return a single object or None.

    If annotation of the reader will be an optional entity class, we should not raise
    DoesNotExist error.  Instead of this we will return None.

    """
    mapper = Mapper(e.User, t.UserTable, {"primary_key": "id"})

    load_user = r.get("load_user_or_none", mapper)

    user1 = load_user(1)

    assert isinstance(user1, e.User)

    user3 = load_user(3)

    assert user3 is None


# Nested mappers.


def test_nested_mapper(e, t, r):
    """Set mapper as a field of another mapper.

    Entities could contains nested entities.  Mappers of nested
    entities should be expressed as nested mappers in the config.

    This code should return a list of `Message` instances.  Each
    `Message` instance should have `User` instance as its attribute.

    """
    mapper = Mapper(
        e.Message,
        t.MessageTable,
        {"primary_key": "id", "user": Mapper({"primary_key": "id"})},
    )

    load_messages = r.get("load_messages", mapper)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.Message)
    assert isinstance(message2, e.Message)
    assert isinstance(message1.user, e.User)
    assert isinstance(message2.user, e.User)


def test_deep_nested_mapper(e, t, r):
    """Set mapper as a field of another field.

    Nested entities could contain nested entities as well.  Mappers of
    nested entities should contain nested mappers as well.

    This code should return a list of `Delivery` instances.  Each
    `Delivery` instance should have `Message` instance as its
    attribute.  Each `Message` instance should have `User` as its
    attribute.

    """
    mapper = Mapper(
        e.Delivery,
        t.DeliveryTable,
        {
            "primary_key": "id",
            "message": Mapper(
                {"primary_key": "id", "user": Mapper({"primary_key": "id"})}
            ),
        },
    )

    load_deliveries = r.get("load_deliveries", mapper)

    result = load_deliveries()

    assert isinstance(result, list)

    delivery1, delivery2 = result

    assert isinstance(delivery1, e.Delivery)
    assert isinstance(delivery2, e.Delivery)
    assert isinstance(delivery1.message, e.Message)
    assert isinstance(delivery2.message, e.Message)
    assert isinstance(delivery1.message.user, e.User)
    assert isinstance(delivery2.message.user, e.User)


# Related fields.


@pytest.mark.parametrize("value", [("user", "name"), ("user", "profile", "login")])
def test_related_field(e, t, r, value):
    """Set field of the related data source to the entity field.

    Mapper could point any field of the entity to any field of any related model of the
    mapped data source.

    """
    mapper = Mapper(
        e.NamedMessage, t.MessageTable, {"primary_key": "id", "username": value}
    )

    load_messages = r.get("load_messages", mapper)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.NamedMessage)
    assert isinstance(message2, e.NamedMessage)
    assert message1.username == ""
    assert message2.username == ""


def test_resolve_id_field_from_foreign_key_without_config(e, t, r):
    """Use foreign key as a field.

    Original data source model could have foreign key field defined.
    The actual entity may require only id value with out whole related
    object.

    Code below should work with out config specifics of the `user`
    field.

    """
    mapper = Mapper(e.FlatMessage, t.MessageTable, {"primary_key": "id"})

    load_messages = r.get("load_messages", mapper)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.FlatMessage)
    assert isinstance(message2, e.FlatMessage)
    assert message1.user_id == 1
    assert message2.user_id == 2


# Evaluated fields.


def test_evaluated_field(e, t, r):
    """Evaluate fields which are not declared in the data source.

    Evaluated marker should be interpreted as a reason to ignore absence of the field
    directly on the data source model.  Field with exactly this name will appears on the
    collection.

    """
    mapper = Mapper(
        e.TotalMessage, t.MessageTable, {"primary_key": "id", "total": Evaluated()}
    )

    load_messages = r.get("load_total_messages", mapper, "total")

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.TotalMessage)
    assert isinstance(message2, e.TotalMessage)
    assert message1.total == 1
    assert message2.total == 1


def test_named_evaluated_field(e, t, r):
    """Use custom name in the data source for the evaluation result.

    Evaluated marker could be pointed to the field with a different name than the target
    attribute.

    """
    mapper = Mapper(
        e.TotalMessage,
        t.MessageTable,
        {"primary_key": "id", "total": Evaluated("total_number")},
    )

    load_messages = r.get("load_total_messages", mapper, "total_number")

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.TotalMessage)
    assert isinstance(message2, e.TotalMessage)
    assert message1.total == 1
    assert message2.total == 1
