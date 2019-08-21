import pytest
from docstring_parser import parse

from .services import jira_test_service, get_current_time


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    item.test_outcome = outcome.get_result()


def pytest_addoption(parser):
    parser.addoption('--submit-tests',
                     action='store_true',
                     help='Submit tests to Jira')


_tests = dict()


@pytest.fixture(scope='session', autouse=True)
def after_each_test_run(request):
    yield

    if request.config.getoption('--submit-tests'):
        test_service = jira_test_service()
        for issue_key in _tests.keys():
            # If the issue is closed, we don't need to submit the tests.
            issue = test_service.get_issue_info(issue_key)

            # if issue['fields']['status']['name'] == 'Closed':
            #     continue
            # First, delete all tests associate with this issue key on TSM.
            tests = test_service.get_tests_in_issue(issue_key)
            # for _, test_key in tests:
            #     test_service.delete_test(test_key)
            # Or first, delete all tests have name exist
            for _, test_key in tests:
                for i in range(len(_tests[issue_key])):
                    if (_ == _tests[issue_key][i]['name']):
                        test_service.delete_test(test_key)

            # Second, for each tests have found by pytest,
            # associate with this issue key, create and update its testCaseKey.
            for test in _tests[issue_key]:
                test_key = test_service.create_test(issue_key, test)
                test['testCaseKey'] = test_key

            # Third, create a test cycle for current issue key on TSM.
            cycle_items = [{
                key: item[key]
                for key in ['testCaseKey', 'status']
            } for item in _tests[issue_key]]
            name = issue_key + ' ' + get_current_time()
            test_service.create_test_cycle(issue_key, name, cycle_items)
            # Last, transition status of task is Production if status of task is Ready for TEST
            status = list()
            for j in range(len(_tests[issue_key])):
                status.append(_tests[issue_key][j]['status'])
            # print(status)
            if 'Fail' in status:
                break
            elif issue['fields']['status']['name'] == 'Ready for TEST':
                test_service.transition_status_task(issue_key)


@pytest.fixture(autouse=True)
def after_each_test_case(request):
    yield

    if request.config.getoption('--submit-tests'):
        docstring = parse(request._pyfuncitem._obj.__doc__)
        STEP_STRING = 'Step by step:'
        if docstring.long_description and STEP_STRING in docstring.long_description:
            objective, steps = map(
                str.strip, docstring.long_description.split(STEP_STRING, 1))
            steps = '<pre>' + steps + '</pre>'
        else:
            objective = docstring.long_description
            steps = None

        name = (docstring.short_description or request._pyfuncitem.name)[:255]
        status = 'Fail' if request.node.test_outcome.failed else 'Pass'

        cls_issue_key = request.cls and request.cls.ISSUE_KEY
        # TODO: Each test case can have some addition issue keys.
        func_issue_keys = []
        issue_keys = [cls_issue_key] + func_issue_keys
        issue_keys = [item for item in issue_keys if item is not None]

        for issue_key in issue_keys:
            if not _tests.get(issue_key):
                _tests[issue_key] = []
            _tests[issue_key].append({
                'name': name,
                'objective': objective,
                'testScript': {
                    'type': 'PLAIN_TEXT',
                    'text': steps
                },
                'status': status
            })
