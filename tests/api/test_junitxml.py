import random

from tests.api.test_results import BaseSuiteResultTest
from tests.junitxml_utils import get_junit_xml_string


class TestJunitXmlSuiteResults(BaseSuiteResultTest):

    def setUp(self):
        super(TestJunitXmlSuiteResults, self).setUp()
        self.junit_xml_string = get_junit_xml_string(
            n_passes=5,
            n_skips=5,
            n_fails=5,
            n_errors=5,
        )
        self.build_num = random.randint(1, 99999999)

    def test_post_junit_xml(self):
        resp = self._create_junit_xml_results(
            self.project_id, self.suite_id, self.junit_xml_string,
            build_num=self.build_num,
        )
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')
