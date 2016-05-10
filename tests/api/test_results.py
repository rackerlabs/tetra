from tests.base import BaseTetraTest


class BaseSuiteResultTest(BaseTetraTest):

    def setUp(self):
        super(BaseSuiteResultTest, self).setUp()

        # setup a project, suite, and build
        resp = self._create_project()
        self.project_id = resp.json()['id']

        resp = self._create_suite(self.project_id)
        self.suite_id = resp.json()['id']

        resp = self._create_build(self.project_id, self.suite_id)
        self.build_id = resp.json()['id']
        self.build_num = resp.json()['build_num']


class TestSuiteResults(BaseSuiteResultTest):

    def setUp(self):
        super(TestSuiteResults, self).setUp()

        self.test_name = "test-name"
        self.result = "passed"
        self.create_resp = self._create_suite_result(
            self.project_id, self.suite_id, test_name=self.test_name,
            result=self.result, build_num=self.build_num,
        )
        self.result_id = self.create_resp.json()['id']

    def test_list_suite_results(self):
        resp = self.client.list_suite_results(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_suite_result(self):
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'passed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('region', self.create_resp.json())
        self.assertIn('environment', self.create_resp.json())
        self.assertIn('build_url', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())
        self.assertIn('extra_data', self.create_resp.json())

    def test_get_suite_result(self):
        resp = self.client.get_suite_result(self.project_id, self.suite_id,
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

    def test_delete_suite_result(self):
        resp = self.client.delete_suite_result(self.project_id, self.suite_id,
                                               self.result_id)
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get_suite_result(self.project_id, self.suite_id,
                                            self.result_id)
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): delete the result again returns a 204
        # resp = self.client.delete_suite_result(self.project_id,
        #                                        self.suite_id, self.result_id)
        # self.assertEqual(resp.status_code, 404)

    def test_delete_suite_with_results(self):
        resp = self.client.delete_suite(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 204)

        # check the suite is gone
        resp = self.client.get_suite(self.project_id, self.suite_id)
        self.assertEqual(resp.status_code, 404)

        # check the result is gone
        resp = self.client.get_suite_result(self.project_id, self.suite_id,
                                            self.result_id)
        self.assertEqual(resp.status_code, 404)


class TestSuiteResultsPagination(BaseSuiteResultTest):

    def setUp(self):
        super(TestSuiteResultsPagination, self).setUp()

        # create 4 results - two passes and two fails.
        self.result_ids = []
        for i in range(4):
            test_name = "test%s" % i
            result = "passed" if i % 2 == 0 else "failed"
            resp = self._create_suite_result(
                self.project_id, self.suite_id, test_name=test_name,
                result=result, build_num=self.build_num,
            )
            self.result_ids.append(resp.json()['id'])

        self.n_results = len(self.result_ids)

    def _checkResultsResp(self, resp, n_results):
        self.assertEqual(resp.status_code, 200)

        results = resp.json()['results']
        self.assertEqual(len(results), n_results)

        metadata = resp.json()['metadata']
        self.assertEqual(metadata['total_results'], self.n_results)
        self.assertEqual(metadata['total_passed'], self.n_results / 2)
        self.assertEqual(metadata['total_failures'], self.n_results / 2)
        self.assertEqual(metadata['total_skipped'], 0)
        self.assertEqual(metadata['success_rate'], 50.00)

    def test_list_suite_results_limit(self):
        # check that all results are returned with no limit
        resp = self.client.list_suite_results(self.project_id, self.suite_id)
        self._checkResultsResp(resp, self.n_results)

        # check limit <= number of results
        for limit in range(self.n_results + 1):
            resp = self.client.list_suite_results(
                self.project_id, self.suite_id, params={'limit': limit},
            )
            self._checkResultsResp(resp, limit)

        # check limit > number of results
        for limit in range(self.n_results + 1, self.n_results + 4):
            resp = self.client.list_suite_results(
                self.project_id, self.suite_id, params={'limit': limit},
            )
            self._checkResultsResp(resp, self.n_results)

    def test_list_suite_results_offset(self):
        # check offset < number of results
        for offset in range(self.n_results):
            resp = self.client.list_suite_results(
                self.project_id, self.suite_id, params={'offset': offset},
            )
            self._checkResultsResp(resp, n_results=self.n_results - offset)

        # check offset >= number of results (returns no results)
        for offset in range(self.n_results, self.n_results + 4):
            resp = self.client.list_suite_results(
                self.project_id, self.suite_id, params={'offset': offset}
            )
            self._checkResultsResp(resp, n_results=0)

    def test_list_suite_results_with_limit_and_offset(self):
        for limit in range(self.n_results):
            for offset in range(self.n_results):
                resp = self.client.list_suite_results(
                    self.project_id, self.suite_id,
                    params={'offset': offset, 'limit': limit},
                )
                self.assertEqual(resp.status_code, 200)

                actual_ids = [x['id'] for x in resp.json()['results']]
                expected_ids = self.result_ids[offset:offset + limit]

                self.assertEqual(actual_ids, expected_ids)
