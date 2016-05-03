import random

from tests.base import BaseTetraTest

class BaseBuildsTest(BaseTetraTest):

    def setUp(self):
        super(BaseBuildsTest, self).setUp()

        resp = self._create_project()
        self.project_id = resp.json()['id']

        resp = self._create_suite(self.project_id)
        self.suite_id = resp.json()['id']

        self.build_num = random.randint(1, 9999999)
        self.create_resp = self._create_build(
            self.project_id, self.suite_id, build_num=self.build_num,
            timestamp=512345,
        )
        self.build = self.create_resp.json()


class TestBuilds(BaseBuildsTest):

    def test_list_builds(self):
        resp = self.client.list_builds(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_get_build(self):
        resp = self.client.get_build(self.project_id, self.suite_id,
                                     self.build['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.build)

    def test_create_build(self):
        self.assertEqual(self.create_resp.json()['timestamp'], 512345)
        self.assertEqual(self.create_resp.json()['build_num'], self.build_num)

    def test_delete_build(self):
        resp = self.client.delete_build(self.project_id, self.suite_id,
                                        self.build['id'])
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text.strip(), '')

        resp = self.client.get_build(self.project_id, self.suite_id,
                                     self.build['id'])
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): deleting a second time returns a 204 also
        # resp = self.client.delete_build(self.project_id, self.suite_id,
        #                                 self.build['id'])
        # self.assertEqual(resp.status_code, 404)


class TestBuildResults(BaseBuildsTest):

    def setUp(self):
        super(TestBuildResults, self).setUp()

        self.build_id = self.build['id']

        self.test_name = "test-name"
        self.result = "failed"
        self.create_resp = self._create_build_result(
            self.project_id, self.suite_id, self.build_id,
            test_name=self.test_name, result=self.result,
            build_num=self.build_num,
        )
        self.result_id = self.create_resp.json()['id']

    def test_list_build_results(self):
        resp = self.client.list_build_results(self.project_id, self.suite_id,
                                              self.build_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_build_result(self):
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'failed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('region', self.create_resp.json())
        self.assertIn('environment', self.create_resp.json())
        self.assertIn('build_url', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())
        self.assertIn('extra_data', self.create_resp.json())

    def test_get_build_result(self):
        resp = self.client.get_build_result(self.project_id, self.suite_id,
                                            self.build_id, self.result_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'failed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('region', self.create_resp.json())
        self.assertIn('environment', self.create_resp.json())
        self.assertIn('build_url', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())
        self.assertIn('extra_data', self.create_resp.json())

    def test_delete_build_result(self):
        resp = self.client.delete_build_result(self.project_id, self.suite_id,
                                               self.build_id, self.result_id)
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get_build_result(self.project_id, self.suite_id,
                                            self.build_id, self.result_id)
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): deleting twice results in a 204
        # resp = self.client.delete_build_result(self.project_id, self.suite_id,
        #                                        self.build_id, self.result_id)
        # self.assertEqual(resp.status_code, 404)
