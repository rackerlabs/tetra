from tests.base import BaseTetraTest


class TestResults(BaseTetraTest):

    def setUp(self):
        super(TestResults, self).setUp()

        resp = self._create_project()
        self.project_id = resp.json()['id']

        resp = self._create_suite(self.project_id)
        self.suite_id = resp.json()['id']

        resp = self._create_build(self.project_id, self.suite_id)
        self.build_id = resp.json()['id']
        self.build_num = resp.json()['build_num']

        self.test_name = "test-name"
        self.result = "passed"
        self.create_resp = self._create_result(
            self.project_id, self.suite_id, test_name=self.test_name,
            result=self.result, build_num=self.build_num,
        )
        self.result_id = self.create_resp.json()['id']

    def test_list_results(self):
        resp = self.client.list_results(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_result(self):
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'passed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('region', self.create_resp.json())
        self.assertIn('environment', self.create_resp.json())
        self.assertIn('build_url', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())
        self.assertIn('extra_data', self.create_resp.json())

    def test_get_result(self):
        resp = self.client.get_result(self.project_id, self.suite_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'passed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('region', self.create_resp.json())
        self.assertIn('environment', self.create_resp.json())
        self.assertIn('build_url', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())
        self.assertIn('extra_data', self.create_resp.json())

    def test_delete_result(self):
        resp = self.client.delete_result(self.project_id, self.suite_id,
                                         self.result_id)
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get_result(self.project_id, self.suite_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): delete the result again returns a 204
        # resp = self.client.delete_result(self.project_id, self.suite_id,
        #                                  self.result_id)
        # self.assertEqual(resp.status_code, 404)

    def test_delete_suite_with_results(self):
        resp = self.client.delete_suite(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 204)

        # check the suite is gone
        resp = self.client.get_suite(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 404)

        # check the result is gone
        resp = self.client.get_result(self.project_id, self.suite_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 404)
