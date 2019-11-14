import operator
from typing import List
from typing import Optional


class Evaluated(object):
    def __init__(self, name=None):
        self.name = name


class LazyMapper(object):
    def __init__(self, config):
        self.config = config

    def build(self, entity, data_source):
        from _mappers.factory import mapper_factory

        return mapper_factory(entity, data_source, self.config)


class Mapper(object):
    def __init__(self, entity, data_source, config, iterable):
        self.entity = entity
        self.data_source = data_source
        self.config = config
        self.iterable = iterable

    @property
    def reader(self):
        return ReaderGetter(self.iterable, self.entity)


class ReaderGetter(object):
    def __init__(self, iterable, entity):
        self.iterable = iterable
        self.entity = entity
        self.ret = None

    def __call__(self, f):
        if self.ret is None:
            self.ret = f.__annotations__["return"]
        return Reader(f, self.iterable, self.entity, self.ret)

    def of(self, ret):
        self.ret = ret
        return self


class Reader(object):
    def __init__(self, f, iterable, entity, ret):
        self.f = f
        self.iterable = iterable
        self.converter = get_converter(ret, entity)

    def __call__(self, *args, **kwargs):
        return self.converter(self.raw(*args, **kwargs))

    def raw(self, *args, **kwargs):
        return self.iterable(self.f(*args, **kwargs))


def get_converter(ret, entity):
    if ret is entity:
        return operator.methodcaller("get")
    elif ret == List[entity]:
        return list
    elif ret == Optional[entity]:
        return operator.methodcaller("first")
    else:
        return lambda x: x
