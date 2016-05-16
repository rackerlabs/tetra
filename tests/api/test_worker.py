from tests.base import BaseTetraTest


class TestWorker(BaseTetraTest):

    def test_workers_ping(self):
        resp = self.client.workers_ping()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['result'], 7374)
