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

        # TODO(pglass): tetra can't delete projects
        # self.addCleanup(self.client.delete_project, resp.json()['id'])
        return resp

    def _create_suite(self, project_id, name=None, description=None):
        data = {
            'name': name or "test-suite",
            'description': description or "this is a test suite",
        }

        resp = self.client.create_suite(project_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_suite, project_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        return resp

    def _create_build(self, project_id, suite_id, build_num=None,
                      timestamp=None):
        data = {'build_num': build_num or random.randint(1, 9999999)}
        if timestamp is not None:
            data['timestamp'] = timestamp

        resp = self.client.create_build(project_id, suite_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_build, project_id, suite_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        self.assertEqual(resp.json()['suite_id'], suite_id)
        return resp

    def _create_suite_result(self, project_id, suite_id, test_name, result,
                             build_num, timestamp=None, region=None,
                             environment=None, build_url=None,
                             result_message=None, extra_data=None):
        data = self._get_result_data(project_id, suite_id, test_name, result,
                                     build_num, timestamp, region, environment,
                                     build_url, result_message, extra_data)
        resp = self.client.create_suite_result(project_id, suite_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_suite_result, project_id, suite_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        self.assertEqual(resp.json()['suite_id'], suite_id)
        return resp

    def _create_build_result(self, project_id, suite_id, build_id, test_name,
                             result, build_num, timestamp=None, region=None,
                             environment=None, build_url=None,
                             result_message=None, extra_data=None):
        data = self._get_result_data(project_id, suite_id, test_name, result,
                                     build_num, timestamp, region, environment,
                                     build_url, result_message, extra_data)
        resp = self.client.create_build_result(project_id, suite_id, build_id,
                                               data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_build_result, project_id, suite_id,
                        build_id, resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        self.assertEqual(resp.json()['suite_id'], suite_id)
        return resp

    def _get_result_data(self, project_id, suite_id, test_name, result,
                         build_num, timestamp=None, region=None,
                         environment=None, build_url=None,
                         result_message=None, extra_data=None):
        data = {
            'test_name': test_name or "name of the test!",
            'result': result or random.choice(['passed', 'failed']),
            'build_num': build_num or random.randint(1, 9999999),
            'timestamp': timestamp,
            'region': region,
            'environment': environment,
            'build_url': build_url,
            'result_message': result_message,
            'extra_data': extra_data,
        }
        # remove all the none values
        return {k: v for k, v in data.items() if v is not None}
