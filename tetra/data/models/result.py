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

from sqlalchemy.sql import func, select

from tetra.data import sql
from tetra.data.db_handler import get_handler
from tetra.data.models.base import BaseModel


class Result(BaseModel):

    TABLE = sql.results_table

    def __init__(self, test_name, result, project_id, suite_id, build_num,
                 id=None, timestamp=None,  result_message=None, region=None,
                 environment=None, build_url=None, extra_data=None):
        if id:
            self.id = id
        self.test_name = test_name
        self.project_id = project_id
        self.suite_id = suite_id
        self.build_num = build_num
        self.timestamp = timestamp or time.time()
        self.result = result
        max_message = self.TABLE.c.result_message.type.length
        if result_message and len(result_message) > max_message:
            result_message = result_message[0:max_message]
        self.result_message = result_message
        self.region = region
        self.environment = environment
        self.build_url = build_url
        self.extra_data = extra_data

    @classmethod
    def get_all(cls, handler=None, **kwargs):
        handler = handler or get_handler()
        results = super(cls, Result).get_all(handler=None, **kwargs)

        query = select(
            [cls.TABLE.c.result, func.count(cls.TABLE.c.result).label("count")]
        ).where(cls._and_clause(**kwargs)).group_by(cls.TABLE.c.result)
        count_results = handler.get_all(resource_class=Result, query=query)

        total_results = len(results)
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        total_passed = 0

        for result in count_results:
            if result.get("result").lower() == "failure":
                total_failures += result.get("count")
            elif result.get("result").lower() == "error":
                total_errors += result.get("count")
            elif result.get("result").lower() == "skipped":
                total_skipped += result.get("count")
            else:
                total_passed += result.get("count")

        success_rate = 0
        if total_results > 0:
            success_rate = (total_passed / float(total_results - total_skipped)
                            * 100)
            success_rate = float("{0:.1f}".format(success_rate))

        metadata = {
            "total_results": total_results,
            "total_passed": total_passed,
            "total_failures": total_failures,
            "total_errors": total_errors,
            "total_skipped": total_skipped,
            "success_rate": success_rate
        }

        results_dict = {
            "results": results,
            "metadata": metadata
        }

        return results_dict
