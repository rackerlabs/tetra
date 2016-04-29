from tests.base import BaseTetraTest


class TestSuites(BaseTetraTest):

    def setUp(self):
        super(TestSuites, self).setUp()

        resp = self._create_project()
        self.project_id = resp.json()['id']

        self.create_resp = self._create_suite(self.project_id,
                                              name='test-suite',
                                              description='a test suite')
        self.suite = self.create_resp.json()

    def test_list_suites(self):
        resp = self.client.list_suites(self.project_id)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_get_suite(self):
        resp = self.client.get_suite(self.project_id, self.suite['id'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.suite)

    def test_create_suite(self):
        self.assertEqual(self.suite['name'], 'test-suite')
        self.assertEqual(self.suite['description'], 'a test suite')

    def test_delete_suite(self):
        resp = self.client.delete_suite(self.project_id, self.suite['id'])
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text.strip(), '')

        resp = self.client.get_suite(self.project_id, self.suite['id'])
        self.assertEqual(resp.status_code, 404)

        # TODO(pglass): deleting an already-deleted suite returns a 204
        # resp = self.client.delete_suite(self.project_id, self.suite['id'])
        # self.assertEqual(resp.status_code, 404)
