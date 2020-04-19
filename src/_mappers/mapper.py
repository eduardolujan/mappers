# -*- coding: utf-8 -*-
from operator import methodcaller


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


class _ReaderGetter(object):
    def __init__(self, iterable):
        self._iterable = iterable

    def entity(self, f):
        return _Reader(f, self._iterable, methodcaller("get"))

    def optional(self, f):
        return _Reader(f, self._iterable, methodcaller("first"))

    def sequence(self, f):
        return _Reader(f, self._iterable, list)


class _Reader(object):
    def __init__(self, f, iterable, converter):
        self.f = f
        self.iterable = iterable
        self.converter = converter

    def __call__(self, *args, **kwargs):
        return self.converter(self.raw(*args, **kwargs))

    def raw(self, *args, **kwargs):
        return self.iterable(self.f(*args, **kwargs))
