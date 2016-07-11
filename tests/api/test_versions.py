from tests.base import BaseTetraTest


class TestVersion(BaseTetraTest):

    def setUp(self):
        super(TestVersion, self).setUp()

    def test_list_projects(self):
        resp = self.client.list_versions()
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)
