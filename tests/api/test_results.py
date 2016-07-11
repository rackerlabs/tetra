from tests.base import BaseTetraTest


class BaseResultTest(BaseTetraTest):

    def setUp(self):
        super(BaseResultTest, self).setUp()

        # setup a project and build
        resp = self._create_project()
        self.project_id = resp.json()['id']

        resp = self._create_build(self.project_id)
        self.build_id = resp.json()['id']


class TestResults(BaseResultTest):

    def setUp(self):
        super(TestResults, self).setUp()

        self.test_name = "test-name"
        self.result = "passed"
        self.create_resp = self._create_result(
            self.project_id, self.build_id, test_name=self.test_name,
            result=self.result
        )
        self.result_id = self.create_resp.json()['id']

    def test_list_project_results(self):
        resp = self.client.list_project_results(self.project_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_list_results(self):
        resp = self.client.list_results(self.project_id, self.build_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_result(self):
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'passed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())

    def test_get_result(self):
        resp = self.client.get_result(self.project_id, self.build_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.create_resp.json()['test_name'], self.test_name)
        self.assertEqual(self.create_resp.json()['result'], 'passed')
        self.assertIn('timestamp', self.create_resp.json())
        self.assertIn('result_message', self.create_resp.json())

    def test_delete_result(self):
        resp = self.client.delete_result(self.project_id, self.build_id,
                                         self.result_id)
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get_result(self.project_id, self.build_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): delete the result again returns a 204
        # resp = self.client.delete_result(self.project_id,
        #                                        self.build_id, self.result_id)
        # self.assertEqual(resp.status_code, 404)

    def test_delete_build_with_results(self):
        resp = self.client.delete_build(self.project_id, self.build_id)
        self.assertEqual(resp.status_code, 204)

        # check the build is gone
        resp = self.client.get_build(self.project_id, self.build_id)
        self.assertEqual(resp.status_code, 404)

        # check the result is gone
        resp = self.client.get_result(self.project_id, self.build_id,
                                      self.result_id)
        self.assertEqual(resp.status_code, 404)


class TestResultsPagination(BaseResultTest):

    def setUp(self):
        super(TestResultsPagination, self).setUp()

        # create 4 results - two passes and two fails.
        self.result_ids = []
        for i in range(4):
            test_name = "test%s" % i
            result = "passed" if i % 2 == 0 else "failed"
            resp = self._create_result(
                self.project_id, self.build_id, test_name=test_name,
                result=result,
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

    def test_list_results_limit(self):
        # check that all results are returned with no limit
        resp = self.client.list_results(self.project_id, self.build_id)
        self._checkResultsResp(resp, self.n_results)

        # check limit <= number of results
        for limit in range(self.n_results + 1):
            resp = self.client.list_results(
                self.project_id, self.build_id, params={'limit': limit},
            )
            self._checkResultsResp(resp, limit)

        # check limit > number of results
        for limit in range(self.n_results + 1, self.n_results + 4):
            resp = self.client.list_results(
                self.project_id, self.build_id, params={'limit': limit},
            )
            self._checkResultsResp(resp, self.n_results)

    def test_list_results_offset(self):
        # check offset < number of results
        for offset in range(self.n_results):
            resp = self.client.list_results(
                self.project_id, self.build_id, params={'offset': offset},
            )
            self._checkResultsResp(resp, n_results=self.n_results - offset)

        # check offset >= number of results (returns no results)
        for offset in range(self.n_results, self.n_results + 4):
            resp = self.client.list_results(
                self.project_id, self.build_id, params={'offset': offset}
            )
            self._checkResultsResp(resp, n_results=0)

    def test_list_results_with_limit_and_offset(self):
        for limit in range(self.n_results):
            for offset in range(self.n_results):
                resp = self.client.list_results(
                    self.project_id, self.build_id,
                    params={'offset': offset, 'limit': limit},
                )
                self.assertEqual(resp.status_code, 200)

                actual_ids = [x['id'] for x in resp.json()['results']]
                expected_ids = self.result_ids[offset:offset + limit]

                self.assertEqual(actual_ids, expected_ids)
