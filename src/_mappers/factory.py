from _mappers.entities import _entity_factory
from _mappers.exceptions import MapperError
from _mappers.mapper import _LazyMapper
from _mappers.mapper import _Mapper
from _mappers.sources import _data_source_factory
from _mappers.validation import _validate


def mapper_factory(entity=None, data_source=None, config=None):
    """Define declarative mapper from data source to domain entity."""
    entity, data_source, config = _decompose(entity, data_source, config)
    if not isinstance(config, dict):
        raise MapperError
    if entity and data_source:
        iterable = _configure(entity, data_source, config)
        return _Mapper(entity, data_source, config, iterable)
    else:
        return _LazyMapper(config)


def _decompose(first, second, third):
    if first is None and second is None and third is None:
        return None, None, {}
    elif isinstance(first, dict) and second is None and third is None:
        return None, None, first
    elif first is not None and second is not None:
        return first, second, third or {}
    else:
        raise MapperError


def _configure(entity, data_source, config):
    fields, entity_factory = _entity_factory(entity)
    data_source_fields, data_source_factory = _data_source_factory(data_source)
    mapping = _validate(dict(fields), data_source_fields, config, data_source)
    iterable = data_source_factory(fields, entity_factory, mapping)
    return iterable
