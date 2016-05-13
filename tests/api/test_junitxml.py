import random

from tests.api.test_results import BaseResultTest
from tests.junitxml_utils import get_junit_xml_string


class TestJunitXmlResults(BaseResultTest):

    def setUp(self):
        super(TestJunitXmlResults, self).setUp()
        self.junit_xml_string = get_junit_xml_string(
            n_passes=3,
            n_skips=4,
            n_fails=5,
            n_errors=6,
        )
        self.build_num = random.randint(1, 99999999)

    def test_post_junit_xml(self):
        # post the results to the same build num two times. the metadata only
        # represents the newly-created results, so it be the same both times.
        for _ in range(2):
            resp = self._create_junit_xml_results(
                self.project_id, self.build_id, self.junit_xml_string
            )

            metadata = resp.json()['metadata']
            self.assertEqual(metadata['total_passed'], 3)
            self.assertEqual(metadata['total_skipped'], 4)
            self.assertEqual(metadata['total_failures'], 5)
            self.assertEqual(metadata['total_errors'], 6)
            self.assertEqual(metadata['total_results'], 18)
            self.assertEqual(metadata['success_rate'], 21.43)

        # we've posted the same junit xml twice. the metadata returned when
        # listing all results for the build_id should reflect this.
        resp = self.client.list_results(
            self.project_id, self.build_id
        )

        metadata = resp.json()['metadata']
        self.assertEqual(metadata['total_passed'], 6)
        self.assertEqual(metadata['total_skipped'], 8)
        self.assertEqual(metadata['total_failures'], 10)
        self.assertEqual(metadata['total_errors'], 12)
        self.assertEqual(metadata['total_results'], 36)
        self.assertEqual(metadata['success_rate'], 21.43)
