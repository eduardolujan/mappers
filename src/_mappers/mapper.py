# -*- coding: utf-8 -*-


class Evaluated(object):
    """Mark data source field as evaluated at reading time."""

    def __init__(self, name=None):
        self.name = name


class _LazyMapper(object):
    def __init__(self, config):
        self.config = config


class _Mapper(object):
    def __init__(self, entity, data_source, config, iterable):
        self.entity = entity
        self.data_source = data_source
        self.config = config
        self.iterable = iterable

    @property
    def reader(self):
        return _ReaderGetter(self.iterable)


class _Converter(object):
    entity = object()
    optional = object()
    sequence = object()
    iterable = object()


class _ReaderGetter(object):
    def __init__(self, iterable):
        self._iterable = iterable

    def entity(self, f):
        return _Reader(f, self._iterable, _Converter.entity)

    def optional(self, f):
        return _Reader(f, self._iterable, _Converter.optional)

    def sequence(self, f):
        return _Reader(f, self._iterable, _Converter.sequence)

    def iterable(self, f):
        return _Reader(f, self._iterable, _Converter.iterable)


class _Reader(object):
    def __init__(self, f, iterable, converter):
        self._f = f
        self._iterable = iterable
        self._converter = iterable.converters[converter]

    def __repr__(self):
        return "<Reader::{name}>".format(name=self._f.__name__)

    def __call__(self, *args, **kwargs):
        return self._converter(self._iterable(self._f(*args, **kwargs)))
