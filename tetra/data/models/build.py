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
from tetra.data import sql
from tetra.data.models.base import BaseModel

from tetra.config import cfg
from tetra.data import sql
from tetra.data.db_handler import get_handler

from tetra.data.models.tags import Tag

from sqlalchemy import and_, text, select

class Build(BaseModel):

    TABLE = sql.builds_table
    RESOURCE_TAGS_TABLE = sql.build_tags_table

    def __init__(self, project_id, name, id=None, build_url=None, region=None,
                 environment=None):
        if id:
            self.id = int(id)
        self.project_id = int(project_id)
        self.name = name
        self.build_url = build_url
        self.region = region
        self.environment = environment

    @classmethod
    def get_all(cls, handler=None, limit=None, offset=None, project_id=None,
                name=None, build_url=None, region=None, environment=None,
                **kwargs):
        handler = handler or get_handler()
        if kwargs:
            joined_table = cls.TABLE.outerjoin(
                cls.RESOURCE_TAGS_TABLE,
                and_(cls.TABLE.c.id == cls.RESOURCE_TAGS_TABLE.c.build_id)
            ).outerjoin(
                cls.TAGS_TABLE,
                and_(cls.RESOURCE_TAGS_TABLE.c.tag_id == cls.TAGS_TABLE.c.id))

            joined_table = select([
                cls.TABLE,
                cls.TAGS_TABLE.c.key,
                cls.TAGS_TABLE.c.value,
            ]).select_from(joined_table)

            builds_and_clause = cls._and_clause(
                project_id=project_id, name=name,
                build_url=build_url, region=region, environment=environment)
            tables = []
            for i, (key, value) in enumerate(kwargs.iteritems(), 1):
                alias = "t%s" % i
                tag_and_clause = Tag._and_clause(key=key, value=value)
                full_and_clause = and_(tag_and_clause, builds_and_clause)
                table = joined_table.where(full_and_clause).alias(alias)
                tables.append(table)

            mega_table = tables[0]
            for i, table in enumerate(tables[1:], 2):
                mega_table = mega_table.join(table, text("t1.id = t%s.id" % i))

            query = mega_table.select()
            query = query.order_by(text("t1.id"))

            return handler.get_all(resource_class=cls, query=query,
                                   limit=limit, offset=offset)

        else:
            return super(Build, cls).get_all(
                handler=handler, limit=limit, offset=offset,
                project_id=project_id, name=name, build_url=build_url,
                region=region, environment=environment)
