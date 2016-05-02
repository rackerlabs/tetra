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

import xunitparser

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

    def on_get(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_200
        kwargs.update(req.params)
        builds = self.RESOURCE_CLASS.get_all(**kwargs)

        for build in builds:
            results = Result.get_all(project_id=build['project_id'],
                                     suite_id=build['suite_id'],
                                     build_num=build['build_num'])
            build['results'] = results.get("metadata")

        resp.body = json.dumps(builds)

    def on_post(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        project_id = kwargs.get("project_id")
        suite_id = kwargs.get("suite_id")
        data_dict['project_id'] = project_id
        data_dict['suite_id'] = suite_id
        build = Build.from_dict(data_dict)
        created_result = Build.create(resource=build)
        resp.body = json.dumps(created_result.to_dict())


class BuildResource(Resource):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_id}"
    RESOURCE_CLASS = Build
    RESOURCE_ID_KEY = "build_id"


class BuildResultsResource(Resources):
    ROUTE = "/{project_id}/suites/{suite_id}/builds/{build_id}/results"
    RESOURCE_CLASS = Result

    # a result is tied to a build via the build_num only, so we can ignore
    # the build_id when listing or posting results for this route.
    def on_get(self, req, resp, build_id, **kwargs):
        return super(BuildResultsResource, self).on_get(req, resp, **kwargs)

    def on_post(self, req, resp, build_id, **kwargs):
        return super(BuildResultsResource, self).on_post(req, resp, **kwargs)


class BuildResultResource(Resource):
    ROUTE = ("/{project_id}/suites/{suite_id}/builds/{build_id}"
             "/results/{result_id}")
    RESOURCE_CLASS = Result
    RESOURCE_ID_KEY = "result_id"


class SuiteResultsResource(Resources):
    ROUTE = "/{project_id}/suites/{suite_id}/results"
    RESOURCE_CLASS = Result

    def on_post(self, req, resp, **kwargs):
        if req.content_type and 'application/xml' in req.content_type:
            return self._on_post_junitxml(req, resp, **kwargs)
        return super(SuiteResultsResource, self).on_post(req, resp, **kwargs)

    def _on_post_junitxml(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_204
        project_id = kwargs['project_id']
        suite_id = kwargs['suite_id']

        suite, _ = xunitparser.parse(req.stream)
        results = [
            Result.from_junit_xml_test_case(case, req, project_id, suite_id)
            for case in suite
        ]
        Result.create_many(results)


class SuiteResultResource(Resource):
    ROUTE = "/{project_id}/suites/{suite_id}/results/{result_id}"
    RESOURCE_CLASS = Result
    RESOURCE_ID_KEY = "result_id"
