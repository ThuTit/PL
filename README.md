# Submit tests to Jira guideline
A guideline for submit test cases and move Jira issue's status after ready for test.

### Example
```python
from calculator import plus

class TestSimplePlus():
  # You should provide which issue this test suite will be refered to.
  # All tests' result under this suite will be submitted to that issue.
  ISSUE_KEY = 'DP-53'
  
  def test_should_plus_string_correctly():
    # You can define addition info for the test using docstring.
    # Short description (the first line) will be used as test's name.
    # Long description (the rest of docstring) will be used as test's objective.
    # If in long description has string 'Step by step:', 
    # the part after 'Step by step:' will be used as test script in plain text (check tab `Test script` in test details).
    '''
    Plus two strings
    
    This test tests if plus function can concatenate two strings.
    
    Step by step:
    - Init first string: a
    - Init second string: b
    - Call `plus(a, b)` function
    '''
    # Here is your logic of the test
    assert plus('Hello', 'Teko') == 'Hello Teko'
```

### Usage
Include [`conftest.py`](tests/conftest.py) and [`services.py`](tests/services.py) files in your project (under `tests/` folder).

When you write your tests, create test class suite, then add property `ISSUE_KEY` to the class which refers to Jira issue key.

You can also provide more information using `docstring` as described in the example.

For more details, please refer to [`TestSimplePlus`](tests/test_calculator.py)

To submit the tests' result to Jira (which should setup on CI environment):
- Set `JIRA_USERNAME`, `JIRA_PASSWORD` and `JIRA_PROJECT_KEY` in environment.
- Add option `--submit-tests` when run `pytest`.
The script will automatic creates test cases (for each tests in suite) and test cycle (which has the result of running all tests in each suite).


### Limitation
- [`docstring-parser`](https://pypi.org/project/docstring-parser/) is required.
- The script will automatically truncate test name if it is longer than 255 characters (include `parametrize` values). So there will be some tests with same name, if their names only have different after 255th character.
- Test name from docstring does not include `parametrize` values in it. So there will be some tests with same name, if there are `parametrize` values.

### Development
Setup `pipenv` enviroment. Then run:
```
pipenv shell
pipenv install
```

If you find any error within with module, please open a Pull Request.

### Change log
- 2019/06/25:
  - Not re-submit tests if the issue is closed.
  - Simplize intergate logic: remove usage of `JiraTest`, `utils.py`; move `services.py` into separate file; simplize submit test logic.

### Todo
- [ ] Make this project into a pytest plugin.
- [ ] Make each test can submit to multiple issues.
