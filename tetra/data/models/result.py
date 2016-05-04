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
from tetra.data.models.base import BaseModel, DictSerializer


class ResultMetadata(DictSerializer):

    def __init__(self, total_passed, total_failures, total_errors,
                 total_skipped, total_results=None, success_rate=None):
        self.total_passed = int(total_passed)
        self.total_failures = int(total_failures)
        self.total_errors = int(total_errors)
        self.total_skipped = int(total_skipped)

        self.total_results = total_results
        if self.total_results is None:
            self.total_results = sum([self.total_passed, self.total_failures,
                                      self.total_errors, self.total_skipped])

        self.success_rate = success_rate
        if self.success_rate is None:
            self.success_rate = self.compute_success_rate(
                self.total_passed, self.total_skipped, self.total_results)

    @classmethod
    def compute_success_rate(cls, passed, skipped, total):
        success_rate = 0
        if total > 0:
            success_rate = passed / float(total - skipped) * 100
        return round(success_rate, 2)

    @classmethod
    def from_results_list(cls, results):
        """Create a ResultMetadata from a list of Result model objects"""
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        total_passed = 0

        for result in results:
            result_status = result.result

            if "fail" in result_status:
                total_failures += 1
            elif "error" in result_status:
                total_errors += 1
            elif "skip" in result_status:
                total_skipped += 1
            else:
                total_passed += 1

        return ResultMetadata(
            total_passed=total_passed,
            total_skipped=total_skipped,
            total_failures=total_failures,
            total_errors=total_errors,
        )

    @classmethod
    def from_database_counts(cls, count_results):
        """Create a ResultMetadata from any list of dicts that looks like:

            [{"result": "passed", "count": 123}, ...]
        """
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        total_passed = 0

        for result in count_results:
            result_status = result["result"].lower()
            count = result["count"]

            if "fail" in result_status:
                total_failures += count
            elif "error" in result_status:
                total_errors += count
            elif "skip" in result_status:
                total_skipped += count
            else:
                total_passed += count

        return ResultMetadata(
            total_passed=total_passed,
            total_skipped=total_skipped,
            total_failures=total_failures,
            total_errors=total_errors,
        )


class Result(BaseModel):

    TABLE = sql.results_table

    def __init__(self, test_name, result, project_id, suite_id, build_num,
                 id=None, timestamp=None,  result_message=None, region=None,
                 environment=None, build_url=None, extra_data=None):
        if id:
            self.id = int(id)
        self.test_name = test_name
        self.project_id = int(project_id)
        self.suite_id = int(suite_id)
        self.build_num = int(build_num)
        self.timestamp = timestamp or time.time()
        self.result = result
        self.result_message = result_message
        self.region = region
        self.environment = environment
        self.build_url = build_url
        self.extra_data = extra_data

    @classmethod
    def from_junit_xml_test_case(cls, case, req, project_id, suite_id):
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
            suite_id=suite_id,
            build_num=req.get_header('X-Tetra-Build-Num'),
            environment=req.get_header('X-Tetra-Environment'),
            build_url=req.get_header('X-Tetra-Build-Url'),
            region=req.get_header('X-Tetra-Region'),
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
