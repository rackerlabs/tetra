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
from sqlalchemy import and_, text, select

from tetra.data import sql
from tetra.data.db_handler import get_handler
from tetra.data.models.base import BaseModel, truncate
from tetra.data.models.tags import Tag


class Build(BaseModel):

    TABLE = sql.builds_table
    RESOURCE_TAGS_TABLE = sql.build_tags_table

    def __init__(self, project_id, name, id=None, build_url=None, region=None,
                 environment=None):
        if id:
            self.id = int(id)
        self.project_id = int(project_id)
        self.name = truncate(name, self.TABLE.c.name.type.length)
        self.build_url = truncate(build_url,
                                  self.TABLE.c.build_url.type.length)
        self.region = truncate(region, self.TABLE.c.region.type.length)
        self.environment = truncate(environment,
                                    self.TABLE.c.environment.type.length)

    @classmethod
    def get_all(cls, handler=None, limit=None, offset=None, project_id=None,
                name=None, build_url=None, region=None, environment=None,
                **kwargs):
        handler = handler or get_handler()
        if kwargs:
            # Create a table that joins the builds, build tags, and tags
            joined_table = cls.TABLE.outerjoin(
                cls.RESOURCE_TAGS_TABLE,
                and_(cls.TABLE.c.id == cls.RESOURCE_TAGS_TABLE.c.build_id)
            ).outerjoin(
                cls.TAGS_TABLE,
                and_(cls.RESOURCE_TAGS_TABLE.c.tag_id == cls.TAGS_TABLE.c.id))

            # Select only the build info and the key/value tag pairs
            joined_table_select = select([
                cls.TABLE,
                cls.TAGS_TABLE.c.key,
                cls.TAGS_TABLE.c.value,
            ]).select_from(joined_table)

            # Query for the non-tag values as well
            builds_and_clause = cls._and_clause(
                project_id=project_id, name=name,
                build_url=build_url, region=region, environment=environment)

            # Create a table for each tag we're looking for
            tables = []
            for i, (key, value) in enumerate(kwargs.iteritems(), 1):
                alias = "t%s" % i
                tag_and_clause = Tag._and_clause(key=key, value=value)
                full_and_clause = and_(tag_and_clause, builds_and_clause)
                table = joined_table_select.where(full_and_clause).alias(alias)
                tables.append(table)

            # Join all the tag tables together to determine which builds have
            # all the desired tags
            desired_builds_table = tables[0]
            for i, table in enumerate(tables[1:], 2):
                desired_builds_table = desired_builds_table.join(
                    table, text("t1.id = t%s.id" % i))

            # Get all tags for each build that has the desired tags
            # 1.) Join table with desired builds with builds tags table
            # to determine what build tags we care about
            # 2.) Join that table with the tags table to get the key/values
            joined_table_w_tags = desired_builds_table.join(
                cls.RESOURCE_TAGS_TABLE, and_(
                    text("t1.id") == cls.RESOURCE_TAGS_TABLE.c.build_id)
            ).join(
                cls.TAGS_TABLE,
                and_(cls.RESOURCE_TAGS_TABLE.c.tag_id == cls.TAGS_TABLE.c.id)
            ).alias("joined_table_w_tags")

            tags_query = joined_table_w_tags.select()
            build_tag_combinations = handler.get_all(
                resource_class=cls, query=tags_query,
                limit=limit, offset=offset)

            # Map tag key/value pairs to build ids
            build_tags = {}
            for build in build_tag_combinations:
                if build_tags.get(build.get("build_tags_build_id")):
                    tags = build_tags[build.get("build_tags_build_id")]
                    tags[build.get("tags_key")] = build.get("tags_value")
                    build_tags[build.get("build_tags_build_id")] = tags
                else:
                    build_tags[build.get("build_tags_build_id")] = {
                        build.get("tags_key"): build.get("tags_value")}

            # Get desired builds and add their tags before returning
            query = desired_builds_table.select()
            query = query.order_by(text("t1.id"))
            builds = handler.get_all(resource_class=cls, query=query,
                                     limit=limit, offset=offset)
            for build in builds:
                build["tags"] = build_tags.get(build.get("id"))
                del build["key"]
                del build["value"]
            return builds
        else:
            return super(Build, cls).get_all(
                handler=handler, limit=limit, offset=offset,
                project_id=project_id, name=name, build_url=build_url,
                region=region, environment=environment)
