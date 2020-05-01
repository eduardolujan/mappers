# -*- coding: utf-8 -*-
"""Tests related to the config validation."""
import pytest

from mappers import Evaluated
from mappers import Mapper
from mappers.exceptions import MapperError


pytestmark = pytest.mark.django_db


# Validation.


def test_entity_type_validation(t):
    """Entity argument should be a dataclass, pydantic, or attrs class."""
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(object(), t.UserTable)

    message = str(exc_info.value)
    assert message == expected


def test_data_source_type_validation(e):
    """Data source argument should be a Django model."""
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, object())

    message = str(exc_info.value)
    assert message == expected


def test_config_type_validation(e, t):
    """Config argument should be a dict."""
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(object())

    message = str(exc_info.value)
    assert message == expected

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable, object())

    message = str(exc_info.value)
    assert message == expected


def test_config_key_type_validation(e, t):
    """Config keys should be a string."""
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable, {object(): "test"})

    message = str(exc_info.value)
    assert message == expected


def test_config_value_type_validation(e, t):
    """Config value should be a string."""
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable, {"test": object()})

    message = str(exc_info.value)
    assert message == expected


def test_data_source_field_missing(e, t):
    """Detect if data source field set is not complete.

    Raise exception if data source missed some fields required by
    entity.  And there is no configuration related to the field.
    """
    expected = ("Can not find 'primary_key' field in the %s model") % (t.UserTable,)

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable)

    message = str(exc_info.value)
    assert message == expected


def test_unknown_entity_fields(e, t):
    """Config keys should correspond to the entity fields only.

    There is no possibility to have random keys in the config not
    related to the entity.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable, {"age": "created"})

    message = str(exc_info.value)
    assert message == expected


def test_unknown_data_source_fields(e, t):
    """Config values should correspond to the data source fields only.

    There is no possibility to point to the random strings not related
    to the data source.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, t.UserTable, {"avatar": "photo"})

    message = str(exc_info.value)
    assert message == expected


def test_nullable_field_validation(e, t):
    """Detect if data source field breaks the contract.

    Data source cannot have nullable field if corresponding entity
    attribute is not annotated with Optional type.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.Group, t.GroupTable, {"primary_key": "id"})

    message = str(exc_info.value)
    assert message == expected


def test_nullable_field_optional_attribute(e, t, r):
    """Detect if data source field follows the contract.

    Data source can have nullable field if corresponding entity
    attribute annotated with Optional type.
    """
    mapper = Mapper(e.OptionalGroup, t.GroupTable, {"primary_key": "id"})

    load_groups = r.get("load_groups", mapper)

    result = load_groups()

    assert isinstance(result, list)

    group1, group2 = result

    assert isinstance(group1, e.OptionalGroup)
    assert isinstance(group2, e.OptionalGroup)
    assert group1.name is None
    assert group2.name == ""


def test_nullable_field_unknown_type_attribute(e, t, r):
    """Skip data source contract check if entity has unknown type.

    We can not enforce any constrain on the field from data soure we do
    not know what type it should be on the entity.
    """
    mapper = Mapper(e.UnknownGroup, t.GroupTable, {"primary_key": "id"})

    load_groups = r.get("load_groups", mapper)

    result = load_groups()

    assert isinstance(result, list)

    group1, group2 = result

    assert isinstance(group1, e.UnknownGroup)
    assert isinstance(group2, e.UnknownGroup)
    assert group1.name is None
    assert group2.name == ""


def test_nested_entities_validation(e, t):
    """Detect if data source relations breaks the contract.

    If entity have a nested entity as its field, a corresponding data
    source field should be a relation object.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.UserGroup, t.GroupTable, {"primary_key": "id"})

    message = str(exc_info.value)
    assert message == expected


def test_nested_entities_kind_validation(e, t):
    """Detect if data source relations breaks the contract.

    If entity have a nested entity as its field, the corresponding data
    source field should resolve to only one object.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(
            e.UserChat,
            t.ChatTable,
            {"primary_key": "id", "subscribers": Mapper({"primary_key": "id"})},
        )

    message = str(exc_info.value)
    assert message == expected


@pytest.mark.parametrize("value", ["text", Evaluated()])
def test_nested_entities_type_validation(e, t, value):
    """Detect invalid config definition.

    If entity have a nested entity as its field, the mapper cannot have
    config definition of that field which is not a Mapper.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.Message, t.MessageTable, {"primary_key": "id", "user": value})

    message = str(exc_info.value)
    assert message == expected


def test_related_field_validation(e, t):
    """Detect invalid config definition.

    If the mapper defines a related field, a corresponding data source
    field should be a relation object.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(
            e.NamedMessage,
            t.MessageTable,
            {"primary_key": "id", "username": ("text", "name")},
        )

    message = str(exc_info.value)
    assert message == expected


def test_related_field_kind_validation(e, t):
    """Detect invalid config definition.

    If mapper defines related field, the corresponding data source field
    should resolve to only one object.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(
            e.Chat,
            t.ChatTable,
            {"primary_key": "id", "is_hidden": ("subscribers", "name")},
        )

    message = str(exc_info.value)
    assert message == expected


def test_related_field_length_validation(e, t):
    """Detect invalid config definition.

    Related field could not have place in the same data source as its
    entity.  Therefore, related field definition could not have length
    of one.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(
            e.NamedMessage,
            t.MessageTable,
            {"primary_key": "id", "username": ("text",)},
        )

    message = str(exc_info.value)
    assert message == expected


def test_related_field_type_validation(e, t):
    """Detect invalid config definition.

    Related field definition in the mapper config should be a tuple of
    strings.  We can not have arbitrary objects in the field definition.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(
            e.NamedMessage,
            t.MessageTable,
            {"primary_key": "id", "username": ("user", object())},
        )

    message = str(exc_info.value)
    assert message == expected
