import random
import string

from junit_xml import TestSuite, TestCase


def rand_duration():
    return random.randint(0, 120) + random.random()


def rand_string(prefix, size=40):
    text = "".join(
        [random.choice(string.ascii_letters + ' ') for _ in range(size)])
    return "{} {}".format(prefix, text)


def _gen_cases(n_passes, n_fails, n_skips, n_errors):
    result = []
    for i in range(n_passes):
        case = TestCase(name='TestPassed%s' % i,
                        classname='generated.xml.test.case.passes',
                        elapsed_sec=rand_duration())
        result.append(case)

    for i in range(n_skips):
        case = TestCase(name='TestSkipped%s' % i,
                        classname='generated.xml.test.case.skips',
                        elapsed_sec=rand_duration())
        case.add_skipped_info(message=rand_string('skipped!'))
        result.append(case)

    for i in range(n_fails):
        case = TestCase(name='TestFailed%s' % i,
                        classname='generated.xml.test.case.fails',
                        elapsed_sec=rand_duration())
        case.add_failure_info(message=rand_string('failure!'))
        result.append(case)

    for i in range(n_errors):
        case = TestCase(name='TestErrored%s' % i,
                        classname='generated.xml.test.case.errors',
                        elapsed_sec=rand_duration())
        case.add_error_info(message=rand_string('error!'))
        result.append(case)

    return result


def get_junit_xml_string(n_passes=1, n_fails=1, n_skips=1, n_errors=1):
    cases = _gen_cases(n_passes, n_fails, n_skips, n_errors)
    suite = TestSuite("fake-junit-xml-suite", cases)
    return TestSuite.to_xml_string([suite])
