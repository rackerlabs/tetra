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


class Resources(object):
    RESOURCE_CLASS = None

    def on_get(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_200
        kwargs.update(req.params)
        results = self.RESOURCE_CLASS.get_all(**kwargs)
        resp.body = json.dumps(results)

    def on_post(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict.update(kwargs)
        resource = self.RESOURCE_CLASS.from_dict(data_dict)
        created_resource = self.RESOURCE_CLASS.create(resource=resource)
        resp.body = json.dumps(created_resource.to_dict())


class Resource(object):
    RESOURCE_CLASS = None
    RESOURCE_ID_KEY = ""

    def on_get(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_200
        resource_id = kwargs.get(self.RESOURCE_ID_KEY)
        result = self.RESOURCE_CLASS.get(resource_id=resource_id)
        resp.content_type = 'application/json'
        if result:
            resp.body = json.dumps(result.to_dict())
        else:
            resp.status = falcon.HTTP_404
            resp.body = make_error_body(
                "{0} {1} not found.".format(self.RESOURCE_CLASS.__name__,
                                            resource_id))

    def on_delete(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_204
        resource_id = kwargs.get(self.RESOURCE_ID_KEY)
        self.RESOURCE_CLASS.delete(resource_id=resource_id)


class ProjectsResource(Resources):
    ROUTE = "/projects"
    RESOURCE_CLASS = Project


class SuitesResource(Resources):
    ROUTE = "/{project_id}/suites/"
    RESOURCE_CLASS = Suite


class SuiteResource(Resource):
    ROUTE = "/{project_id}/suites/{suite_id}"
    RESOURCE_CLASS = Suite
    RESOURCE_ID_KEY = "suite_id"


class BuildsResource(Resources):
    ROUTE = "/{project_id}/suites/{suite_id}/builds"
    RESOURCE_CLASS = Build

    def on_post(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        project_id = kwargs.get("project_id")
        suite_id = kwargs.get("suite_id")
        data_dict['project_id'] = project_id
        data_dict['suite_id'] = suite_id
        results = Result.get_all(project_id=project_id,
                                 suite_id=suite_id,
                                 build_num=data_dict.get("build_num"))
        data_dict['results'] = json.dumps(results.get("metadata"))
        build = Build.from_dict(data_dict)
        created_result = Build.create(resource=build)
        resp.body = json.dumps(created_result.to_dict())


class BuildResource(object):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_num}"


class BuildResultsResource(Resources):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_num}/results"
    RESOURCE_CLASS = Result


class BuildResultResource(Resource):
    ROUTE = ("/{project_id}/suites/{suite_id}/builds/{build_num}"
             "/results/{result_id}")
    RESOURCE_CLASS = Result
    RESOURCE_ID_KEY = "result_id"


class ResultsResource(Resources):
    ROUTE = "/{project_id}/suites/{suite_id}/results"
    RESOURCE_CLASS = Result
