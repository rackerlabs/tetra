import random

from tests.api.test_results import BaseSuiteResultTest
from tests.junitxml_utils import get_junit_xml_string


class TestJunitXmlSuiteResults(BaseSuiteResultTest):

    def setUp(self):
        super(TestJunitXmlSuiteResults, self).setUp()
        self.junit_xml_string = get_junit_xml_string(
            n_passes=3,
            n_skips=4,
            n_fails=5,
            n_errors=6,
        )
        self.build_num = random.randint(1, 99999999)

    def test_post_junit_xml(self):
        resp = self._create_junit_xml_results(
            self.project_id, self.suite_id, self.junit_xml_string,
            build_num=self.build_num,
        )

        metadata = resp.json()['metadata']
        self.assertEqual(metadata['total_passed'], 3)
        self.assertEqual(metadata['total_skipped'], 4)
        self.assertEqual(metadata['total_failures'], 5)
        self.assertEqual(metadata['total_errors'], 6)
        self.assertEqual(metadata['total_results'], 18)
        # n_pass / (n_total - n_skips) = 3 / (18 - 4) = 3/14 = 21.43
        self.assertEqual(metadata['success_rate'], 21.43)
