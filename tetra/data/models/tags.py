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


class Tag(BaseModel):

    TABLE = sql.tags_table

    def __init__(self, key, value, id=None):
        if id:
            self.id = int(id)
        self.key = key
        self.value = value


class BuildTag(BaseModel):

    TABLE = sql.build_tags_table

    def __init__(self, build_id, tag_id, id=None):
        if id:
            self.id = int(id)
        self.build_id = build_id
        self.tag_id = tag_id


class ResultTag(BaseModel):

    TABLE = sql.result_tags_table

    def __init__(self, result_id, tag_id, id=None):
        if id:
            self.id = int(id)
        self.result_id = result_id
        self.tag_id = tag_id
