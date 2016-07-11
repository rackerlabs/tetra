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

import inspect
import sys
import xunitparser

from tetra.data.models.build import Build
from tetra.data.models.project import Project
from tetra.data.models.result import Result
from tetra.data.models.tags import Tag, BuildTag


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


class BuildsResource(Resources):
    ROUTE = "/projects/{project_id}/builds"
    RESOURCE_CLASS = Build

    def on_post(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_201
        data = req.stream.read()
        data_dict = json.loads(data)
        data_dict.update(kwargs)
        tags_data = None
        if "tags" in data_dict:
            tags_data = data_dict.get("tags")
            del data_dict["tags"]
        resource = self.RESOURCE_CLASS.from_dict(data_dict)
        created_resource = self.RESOURCE_CLASS.create(resource=resource)

        if tags_data:
            build_tags = []
            for key, value in tags_data.iteritems():
                existing_tags = Tag.get_all(key=key, value=value)
                if len(existing_tags) == 0:
                    tag = Tag.create(Tag(key=key, value=value))
                    build_tags.append(tag)
                else:
                    build_tags.append(Tag.from_dict(existing_tags[0]))
            for tag in build_tags:
                BuildTag.create(BuildTag(build_id=resource.id, tag_id=tag.id))

        created_dict = created_resource.to_dict()
        created_dict["tags"] = tags_data
        resp.body = json.dumps(created_dict)


class BuildResource(Resource):
    ROUTE = "/projects/{project_id}/builds/{build_id}"
    RESOURCE_CLASS = Build
    RESOURCE_ID_KEY = "build_id"


class ResultsResource(Resources):
    ROUTE = "/projects/{project_id}/builds/{build_id}/results"
    RESOURCE_CLASS = Result

    def on_post(self, req, resp, **kwargs):
        if self._is_junit_xml_request(req):
            return self._on_post_junitxml(req, resp, **kwargs)
        return super(ResultsResource, self).on_post(req, resp, **kwargs)

    def _is_junit_xml_request(self, req):
        return req.content_type and 'application/xml' in req.content_type

    def _on_post_junitxml(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_201

        suite, _ = xunitparser.parse(req.stream)
        results = [
            Result.from_junit_xml_test_case(case, **kwargs)
            for case in suite
        ]
        response_data = Result.create_many(results, **kwargs)
        resp.body = json.dumps(response_data)


class ResultResource(Resource):
    ROUTE = "/projects/{project_id}/builds/{build_id}/results/{result_id}"
    RESOURCE_CLASS = Result
    RESOURCE_ID_KEY = "result_id"
