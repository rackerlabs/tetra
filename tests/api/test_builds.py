from tests.base import BaseTetraTest


class BaseBuildsTest(BaseTetraTest):

    def setUp(self):
        super(BaseBuildsTest, self).setUp()
        resp = self._create_project()
        self.project_id = resp.json()['id']


class TestBuilds(BaseBuildsTest):

    def setUp(self):
        super(TestBuilds, self).setUp()
        self.create_resp = self._create_build(
            self.project_id, name='test-build', build_url='test-url',
            region='test-region', environment='test-env', status='passed')
        self.build = self.create_resp.json()

    def test_list_builds(self):
        resp = self.client.list_builds(self.project_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_get_build(self):
        resp = self.client.get_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.build)

    def test_create_build(self):
        self.assertEqual(self.build['name'], 'test-build')
        self.assertEqual(self.build['build_url'], 'test-url')
        self.assertEqual(self.build['region'], 'test-region')
        self.assertEqual(self.build['environment'], 'test-env')
        self.assertEqual(self.build['status'], 'passed')
        self.assertEqual(self.build['tags'], {})

    def test_delete_build(self):
        resp = self.client.delete_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text.strip(), '')

        resp = self.client.get_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): deleting an already-deleted build returns a 204
        # resp = self.client.delete_build(self.project_id, self.build['id'])
        # self.assertEqual(resp.status_code, 404)


class TestBuildsStringTruncation(BaseBuildsTest):
    """Test that the api truncates user input to fit in database columns"""

    def test_api_truncates_long_build_fields(self):
        long_str = "a" * 257

        create_resp = self._create_build(
            project_id=self.project_id,
            name=long_str,
            build_url=long_str,
            region=long_str,
            environment=long_str,
        )
        build = create_resp.json()

        self.assertEqual(len(build['name']), 256)
        self.assertEqual(len(build['build_url']), 256)
        self.assertEqual(len(build['region']), 256)
        self.assertEqual(len(build['environment']), 256)
