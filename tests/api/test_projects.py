from tests.base import BaseTetraTest


class TestProjects(BaseTetraTest):

    def setUp(self):
        super(TestProjects, self).setUp()
        self.create_resp = self._create_project(name='test-project')

    def test_list_projects(self):
        resp = self.client.list_projects()
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()), 0)

    def test_create_project(self):
        project = self.create_resp.json()
        self.assertEqual(project['name'], 'test-project')
        self.assertIn('id', project)
