from tests.base import BaseTetraTest


class TestWorker(BaseTetraTest):

    def test_workers_ping(self):
        resp = self.client.workers_ping()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json()['result'])
