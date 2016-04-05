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

from tetra.data.models.result import Result


def make_error_body(msg):
    return json.dumps({'error': msg})


class ResultsResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Result.get_all())

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        result = Result.from_dict(data_dict)
        created_result = Result.create(resource=result)
        resp.body = json.dumps(created_result.to_dict())


class ResultResource(object):

    def on_get(self, req, resp, result_id):
        resp.status = falcon.HTTP_200
        try:
            result = Result.get(resource_id=result_id)
            resp.content_type = 'application/json'
            resp.body = json.dumps(result.to_dict())
        except Exception as e:
            resp.status = falcon.HTTP_404
            resp.body = make_error_body(str(e))

    def on_delete(self, req, resp, result_id):
        resp.status = falcon.HTTP_204
        Result.delete(resource_id=result_id)
