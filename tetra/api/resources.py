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

from tetra.data.models.build import Build
from tetra.data.models.project import Project
from tetra.data.models.result import Result
from tetra.data.models.suite import Suite


def make_error_body(msg):
    return json.dumps({'error': msg})


class ProjectsResource(object):
    ROUTE = "/projects"

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Project.get_all())

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        project = Project.from_dict(data_dict)
        created_result = Project.create(resource=project)
        resp.body = json.dumps(created_result.to_dict())


class SuitesResource(object):
    ROUTE = "/{project_id}/suites/"

    def on_get(self, req, resp, project_id):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Suite.get_all(project_id=project_id))

    def on_post(self, req, resp, project_id):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict['project_id'] = project_id
        suite = Suite.from_dict(data_dict)
        created_result = Suite.create(resource=suite)
        resp.body = json.dumps(created_result.to_dict())


class SuiteResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}"


class BuildsResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}/builds"

    def on_get(self, req, resp, project_id, suite_id):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Build.get_all(project_id=project_id,
                                             suite_id=suite_id))

    def on_post(self, req, resp, project_id, suite_id):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict['project_id'] = project_id
        data_dict['suite_id'] = suite_id
        build = Build.from_dict(data_dict)
        created_result = Build.create(resource=build)
        resp.body = json.dumps(created_result.to_dict())


class BuildResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_num}"


class BuildResultsResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_num}/results"

    def on_get(self, req, resp, project_id, suite_id, build_num):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Result.get_all(project_id=project_id,
                                              suite_id=suite_id,
                                              build_num=build_num))

    def on_post(self, req, resp, project_id, suite_id, build_num):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict['project_id'] = project_id
        data_dict['suite_id'] = suite_id
        data_dict['build_num'] = build_num
        result = Result.from_dict(data_dict)
        created_result = Result.create(resource=result)
        resp.body = json.dumps(created_result.to_dict())


class BuildResultResource(object):
    ROUTE = ("/{project_id}/suites/{suite_id}/builds/{build_num}"
             "/results/{result_id}")

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


class ResultsResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}/results"

    def on_get(self, req, resp, project_id, suite_id):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(Result.get_all(project_id=project_id,
                                              suite_id=suite_id))

    def on_post(self, req, resp, project_id, suite_id):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict['project_id'] = project_id
        data_dict['suite_id'] = suite_id
        result = Result.from_dict(data_dict)
        created_result = Result.create(resource=result)
        resp.body = json.dumps(created_result.to_dict())
