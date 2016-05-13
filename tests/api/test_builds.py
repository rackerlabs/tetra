from tests.base import BaseTetraTest


class TestBuilds(BaseTetraTest):

    def setUp(self):
        super(TestBuilds, self).setUp()

        resp = self._create_project()
        self.project_id = resp.json()['id']

        self.create_resp = self._create_build(
            self.project_id, name='test-build', build_url='test-url',
            region='test-region', environment='test-env')
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

    def test_delete_build(self):
        resp = self.client.delete_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text.strip(), '')

        resp = self.client.get_build(self.project_id, self.build['id'])
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): deleting an already-deleted build returns a 204
        # resp = self.client.delete_build(self.project_id, self.build['id'])
        # self.assertEqual(resp.status_code, 404)
