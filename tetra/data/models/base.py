"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from tetra.config import cfg
from tetra.data.db_handler import get_handler


conf = cfg.CONF


def truncate(value, length):
    """Truncate the value (a string) to the given length."""
    if value is None:
        return None
    return value[:length]


class DictSerializer(object):

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return dict(self.__dict__)


class BaseModel(DictSerializer):

    TABLE = None
    RESOURCE_TAGS_TABLE = None

    @classmethod
    def create(cls, resource, handler=None):
        handler = handler or get_handler()
        return handler.create(resource)

    @classmethod
    def create_many(cls, resources, handler=None):
        handler = handler or get_handler()
        return handler.create_many(resources)

    @classmethod
    def get(cls, resource_id, handler=None):
        handler = handler or get_handler()
        return handler.get(resource_id=resource_id, resource_class=cls)

    @classmethod
    def _and_clause(cls, **kwargs):
        kwargs = dict((k, v) for k, v in kwargs.iteritems() if v)
        and_clause = None
        for key, value in kwargs.items():
            if and_clause is None:
                and_clause = (getattr(cls.TABLE.c, key) == value)
            else:
                and_clause &= (getattr(cls.TABLE.c, key) == value)
        return and_clause

    @classmethod
    def _get_all_query(cls, and_clause=None, limit=None, offset=None):
        limit = limit or conf.api.default_limit
        query = cls.TABLE.select()
        if and_clause is not None:
            query = query.where(and_clause)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query.order_by(cls.TABLE.c.id.desc())

    @classmethod
    def get_all(cls, handler=None, limit=None, offset=None, **kwargs):
        handler = handler or get_handler()

        and_clause = cls._and_clause(**kwargs)
        query = cls._get_all_query(
            and_clause=and_clause, limit=limit, offset=offset,
        )

        return handler.get_all(resource_class=cls, query=query, limit=limit,
                               offset=offset)

    @classmethod
    def delete(cls, resource_id, handler=None):
        handler = handler or get_handler()
        return handler.delete(resource_id=resource_id, resource_class=cls)
