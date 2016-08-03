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

from api.resources import (
    BuildResource,
    LastCountByStatusResultsResource,
    ResultResource,
    ResultsResource,
    ProjectResultsResource,
    BuildsResource,
    ProjectsResource,
    ProjectResource,
)
from worker.resources import (
    WorkerPingResource,
)


class VersionResource(object):
    ROUTE = "/"

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        # build a json response based on all ROUTE
        routes = [cl.ROUTE for cl in
                  TetraAPI.RESOURCES]

        version = {
                'version': 'v1',
                'resources': routes
                }
        resp.body = json.dumps(version)


class TetraAPI(falcon.API):

    RESOURCES = [
        BuildResource(),
        ResultsResource(),
        ResultResource(),
        LastCountByStatusResultsResource(),
        ProjectResultsResource(),
        BuildsResource(),
        ProjectsResource(),
        ProjectResource(),
        VersionResource(),
        WorkerPingResource(),
    ]

    def __init__(self):
        super(TetraAPI, self).__init__()
        for resource in self.RESOURCES:
            self.add_route(resource.ROUTE, resource)

application = TetraAPI()
