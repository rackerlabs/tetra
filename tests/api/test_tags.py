from tests.api.test_builds import BaseBuildsTest
from tests.api.test_results import BaseResultTest


class BuildTagsTest(BaseBuildsTest):

    def setUp(self):
        super(BuildTagsTest, self).setUp()
        self.tags = {
            'a': 'aaa',
            'b': 'bbb',
            'c': 'ccc',
        }
        self.create_resp = self._create_build(self.project_id, tags=self.tags)
        self.build = self.create_resp.json()

    def test_create_build_with_tags(self):
        self.assertEqual(self.build['name'], 'test-build')
        self.assertEqual(self.build['build_url'], 'test-url')
        self.assertEqual(self.build['region'], 'test-region')
        self.assertEqual(self.build['environment'], 'test-env')
        self.assertEqual(self.build['tags'], self.tags)

    def test_get_build_with_tags(self):
        resp = self.client.get_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.build)

    def test_list_builds_with_tags(self):
        resp = self.client.list_builds(self.project_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0], self.build)

    def test_filter_build_with_tags(self):
        # create some more builds that will be excluded when we filter
        self._create_build(
            project_id=self.project_id,
            name="no-match",
            tags={"a": "no-match"},
        )

        build_2 = self._create_build(
            project_id=self.project_id,
            name="matches-bbb",
            tags={"b": "bbb"},
        ).json()

        # verify we have three builds
        resp = self.client.list_builds(self.project_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

        # check we can filter on a single tag
        resp = self.client.list_builds(self.project_id, params={'b': 'bbb'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)
        for item in resp.json():
            self.assertEqual(item["tags"]["b"], "bbb")
        # remember: builds are descending by id, by default
        self.assertEqual(resp.json()[0], build_2)
        self.assertEqual(resp.json()[1], self.build)

        # check we can filter on multiple tags (must match all tags)
        resp = self.client.list_builds(
            self.project_id, params={'a': 'aaa', 'b': 'bbb'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0], self.build)

        # check we can filter on the tags and other fields
        resp = self.client.list_builds(
            self.project_id, params={'b': 'bbb', 'name': 'test-build'})
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0], self.build)


class ResultTagsTest(BaseResultTest):

    def setUp(self):
        super(ResultTagsTest, self).setUp()
        self.tags = {
            'a': 'aaa',
            'b': 'bbb',
            'c': 'ccc',
        }
        self.create_resp = self._create_result(
            self.project_id, self.build_id, tags=self.tags)
        self.result = self.create_resp.json()

    def test_create_result_with_tags(self):
        self.assertEqual(self.result['test_name'], 'test-result')
        self.assertIn(self.result['result'], ['passed', 'failed'])
        self.assertEqual(self.result['tags'], self.tags)

    def test_get_result_with_tags(self):
        resp = self.client.get_result(
            self.project_id, self.build_id, self.result['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.result)

    def test_list_results_with_tags(self):
        resp = self.client.list_results(self.project_id, self.build_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['results']), 1)
        self.assertEqual(resp.json()['results'][0], self.result)

    def test_filter_result_with_tags(self):
        # create more results to filter
        self._create_result(
            project_id=self.project_id,
            build_id=self.build_id,
            test_name="no-match-result",
            tags={"a": "don't match this"},
        )

        result_2 = self._create_result(
            project_id=self.project_id,
            build_id=self.build_id,
            tags={"c": "ccc", "d": "ddd"},
        ).json()

        # verify we have three results
        resp = self.client.list_results(self.project_id, self.build_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['results']), 3)

        # check we can filter on a single tag
        resp = self.client.list_results(
            self.project_id, self.build_id, params={'c': 'ccc'})
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['results']
        self.assertEqual(len(results), 2)
        for item in results:
            self.assertEqual(item['tags']['c'], 'ccc')
        # sorted by descending id
        self.assertEqual(results[0], result_2)
        self.assertEqual(results[1], self.result)

        # check filtering an many tags
        resp = self.client.list_results(
            self.project_id, self.build_id, params={'a': 'aaa', 'c': 'ccc'})
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.result)
