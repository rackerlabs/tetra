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

from api.resources import (ProjectsResource, BuildResultsResource,
                           BuildResultResource, SuitesResource, BuildsResource,
                           ResultsResource)


class TetraAPI(falcon.API):

    def __init__(self):
        super(TetraAPI, self).__init__()
        results = ResultsResource()
        build_results = BuildResultsResource()
        build_result = BuildResultResource()
        projects = ProjectsResource()
        suites = SuitesResource()
        builds = BuildsResource()
        self.add_route(projects.ROUTE, projects)
        self.add_route(suites.ROUTE, suites)
        self.add_route(builds.ROUTE, builds)
        self.add_route(results.ROUTE, results)
        self.add_route(build_results.ROUTE, build_results)
        self.add_route(build_result.ROUTE, build_result)


application = TetraAPI()
