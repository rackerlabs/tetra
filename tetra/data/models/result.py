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
import time

from sqlalchemy import desc
from sqlalchemy.sql import func, select, and_

from tetra.data import sql
from tetra.data.db_handler import get_handler
from tetra.data.models.base import BaseModel
from tetra.data.models.build import Build
from tetra.data.models.result_metadata import ResultMetadata


class Result(BaseModel):

    TABLE = sql.results_table

    def __init__(self, test_name, result, project_id, build_id, id=None,
                 timestamp=None,  result_message=None):
        if id:
            self.id = int(id)
        self.test_name = test_name
        self.project_id = int(project_id)
        self.build_id = int(build_id)
        self.timestamp = timestamp or time.time()
        self.result = result
        self.result_message = result_message

    @classmethod
    def from_junit_xml_test_case(cls, case, project_id, build_id):
        if case.success:
            result_type = "passed"
        elif case.skipped:
            result_type = "skipped"
        elif case.failed:
            result_type = "failed"
        elif case.errored:
            result_type = "error"
        else:
            result_type = "unknown"

        return Result(
            test_name=case.id(),
            result=result_type,
            project_id=project_id,
            build_id=build_id,
            result_message=case.trace
        )

    @classmethod
    def get_all(cls, handler=None, limit=None, offset=None, **kwargs):
        handler = handler or get_handler()
        results = super(cls, Result).get_all(handler=handler, limit=limit,
                                             offset=offset, **kwargs)

        metadata = cls._get_results_metadata(handler, **kwargs)

        results_dict = {
            "results": results,
            "metadata": metadata.to_dict(),
        }
        return results_dict

    @classmethod
    def get_last_count_by_status(cls, handler=None, limit=None, offset=None,
                                 **kwargs):
        handler = handler or get_handler()
        if (kwargs and
                'build_name' in kwargs and
                'status' in kwargs and
                'count' in kwargs):

            # select * from results
            # where status = kwargs['status']
            # and build_id in (
            #   select build_id from build
            #   where build_name = kwargs['build_name']
            #   order by build_id desc
            #   limit 5
            # )
            query_by_build_name = select([Build.TABLE.c.id]).select_from(
                    Build.TABLE).where(
                        Build.TABLE.c.name == kwargs['build_name']).order_by(
                                desc(Build.TABLE.c.id)
                            ).limit(
                                kwargs['count']
                            )

            last_count_by_status_query = cls.TABLE.select().where(
                    and_(
                        cls.TABLE.c.result == kwargs['status'],
                        cls.TABLE.c.build_id.in_(query_by_build_name)))

            return handler.get_all(
                resource_class=cls, query=last_count_by_status_query,
                limit=limit, offset=offset)
        else:
            return []

    @classmethod
    def create_many(cls, resources, handler=None, **kwargs):
        handler = handler or get_handler()
        super(cls, Result).create_many(resources, handler=handler)

        metadata = ResultMetadata.from_results_list(resources)

        results_dict = {
            "metadata": metadata.to_dict(),
        }
        return results_dict

    @classmethod
    def _get_results_metadata(cls, handler=None, **kwargs):
        handler = handler or get_handler()

        query = select(
            [cls.TABLE.c.result, func.count(cls.TABLE.c.result).label("count")]
        ).where(cls._and_clause(**kwargs)).group_by(cls.TABLE.c.result)
        count_results = handler.get_all(resource_class=Result, query=query)

        return ResultMetadata.from_database_counts(count_results)
