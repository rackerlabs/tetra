import random
import unittest

from tests.client import TetraClient


class BaseTetraTest(unittest.TestCase):

    def setUp(self):
        super(BaseTetraTest, self).setUp()
        self.client = TetraClient.get()

    def _create_project(self, name=None):
        data = {
            'name': name or 'test-project',
        }
        resp = self.client.create_project(data)
        self.assertEqual(resp.status_code, 201)

        self.addCleanup(self.client.delete_project, resp.json()['id'])
        return resp

    def _create_build(self, project_id, name=None, build_url=None,
                      region=None, environment=None, status=None, tags=None):
        data = {
            'name': name or "test-build",
            'build_url': build_url or "test-url",
            'region': region or "test-region",
            'environment': environment or "test-env",
            'status': status,
        }

        if tags is not None:
            data['tags'] = tags

        resp = self.client.create_build(project_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_build, project_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        return resp

    def _create_result(self, project_id, build_id, test_name=None, result=None,
                       timestamp=None, result_message=None, tags=None):
        data = self._get_result_data(project_id, build_id, test_name, result,
                                     timestamp, result_message, tags=tags)
        resp = self.client.create_result(project_id, build_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_result, project_id, build_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        self.assertEqual(resp.json()['build_id'], build_id)
        return resp

    def _create_junit_xml_results(self, project_id, build_id, xml_string):
        headers = {
            'Content-type': 'application/xml'
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        # there's not a way to clean all these results up, but they will be
        # deleted when the build is deleted.
        resp = self.client.create_result_junit_xml(
            project_id, build_id, xml_string, headers=headers,
        )
        self.assertEqual(resp.status_code, 201)
        return resp

    def _get_result_data(self, project_id, build_id, test_name, result,
                         timestamp=None, result_message=None, tags=None):
        data = {
            'test_name': test_name or "test-result",
            'result': result or random.choice(['passed', 'failed']),
            'timestamp': timestamp,
            'result_message': result_message,
            'tags': tags,
        }
        # remove all the none values
        return {k: v for k, v in data.items() if v is not None}
