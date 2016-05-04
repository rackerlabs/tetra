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
from tetra.data.models.base import DictSerializer


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
