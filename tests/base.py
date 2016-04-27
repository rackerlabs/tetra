import logging
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
        data = {'build_num': build_num or 12345}
        if timestamp is not None:
            data['timestamp'] = timestamp

        resp = self.client.create_build(project_id, suite_id, data)
        self.assertEqual(resp.status_code, 201)
        self.addCleanup(self.client.delete_build, project_id, suite_id,
                        resp.json()['id'])

        self.assertEqual(resp.json()['project_id'], project_id)
        self.assertEqual(resp.json()['suite_id'], suite_id)
        return resp
