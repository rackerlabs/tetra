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
import uuid

from tetra.data.models.base import BaseModel


class Result(BaseModel):

    def __init__(self, test_name, timestamp, result, result_message,
                 extra_data):
        self.id = uuid.uuid4()
        self.test_name = test_name
        self.timestamp = timestamp
        self.result = result
        self.result_message = result_message
        self.extra_data = extra_data
