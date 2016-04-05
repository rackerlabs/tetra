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


class Result(BaseModel):

    TABLE = sql.results_table

    def __init__(self, test_name, timestamp, result, id=None,
                 test_suite=None, test_suite_id=None,
                 result_message=None, extra_data=None):
        if id:
            self.id = id
        self.test_name = test_name
        self.test_suite = test_suite
        self.test_suite_id = test_suite_id
        self.timestamp = timestamp
        self.result = result
        self.result_message = result_message
        self.extra_data = extra_data
