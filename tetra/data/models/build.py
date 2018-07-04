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
from tetra.data.db_handler import get_handler
from tetra.data.models.base import BaseModel, truncate


class Build(BaseModel):

    TABLE = sql.builds_table

    def __init__(self, project_id, name, id=None, build_url=None, region=None,
                 environment=None, status=None, tags=None):
        if id:
            self.id = int(id)
        self.project_id = int(project_id)
        self.name = truncate(name, self.TABLE.c.name.type.length)
        self.build_url = truncate(build_url,
                                  self.TABLE.c.build_url.type.length)
        self.region = truncate(region, self.TABLE.c.region.type.length)
        self.environment = truncate(environment,
                                    self.TABLE.c.environment.type.length)
        self.status = truncate(status, self.TABLE.c.status.type.length)
        self.tags = tags or {}

    @classmethod
    def get_all(cls, handler=None, limit=None, offset=None, project_id=None,
                name=None, build_url=None, region=None, environment=None,
                status=None,
                **tag_filters):
        handler = handler or get_handler()
        and_clause = cls._and_clause(
            project_id=project_id, name=name, build_url=build_url,
            region=region, environment=environment,
        )

        # match the build if its tags are a superset of the filters
        if tag_filters:
            and_clause &= cls.TABLE.c.tags.contains(tag_filters)

        query = cls._get_all_query(
            and_clause=and_clause, limit=limit, offset=offset,
        )
        builds = handler.get_all(resource_class=cls, query=query)

        return builds
