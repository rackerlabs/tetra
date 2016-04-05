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
import falcon
import json

from tetra.data.database_client import DatabaseClient
from tetra.data.models.result import Result


class ResultsResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        result = Result.from_dict(data_dict)
        client = DatabaseClient()
        client.save(resource=result)


class ResultResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_204
