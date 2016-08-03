from tests.base import BaseTetraTest


class TestProjects(BaseTetraTest):

    def setUp(self):
        super(TestProjects, self).setUp()
        self.create_resp = self._create_project(name='test-project')
        self.project = self.create_resp.json()

    def test_list_projects(self):
        resp = self.client.list_projects()
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_project(self):
        self.assertEqual(self.project['name'], 'test-project')
        self.assertIn('id', self.project)

    def test_get_project(self):
        resp = self.client.get_project(self.project['id'])
        self.assertEqual(resp.json(), self.project)

    def test_delete_project(self):
        resp = self.client.delete_project(self.project['id'])
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get_project(self.project['id'])
        self.assertEqual(resp.status_code, 404)


class TestProjectStringTruncation(BaseTetraTest):
    """Test that the api truncates user input to fit in database columns"""

    def test_api_truncates_long_project_fields(self):
        create_resp = self._create_project(name="a" * 257)
        project = create_resp.json()
        self.assertEqual(len(project['name']), 256)
