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

from tetra.data import sql
from tetra.data.db_handler import get_handler
from tetra.data.models.base import BaseModel


class Build(BaseModel):

    TABLE = sql.builds_table

    def __init__(self, project_id, suite_id, build_num,
                 id=None, timestamp=None, results=None):
        if id:
            self.id = id
        self.project_id = project_id
        self.suite_id = suite_id
        self.build_num = build_num
        self.timestamp = timestamp or time.time()
        self.total_results = len(results)
        self.total_failures = None
