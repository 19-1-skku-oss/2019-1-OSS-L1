---
layout: post
title: "Parametrizing fixtures and test functions"
summary: Chapter 13
featured-img: parametrize
---
## Chapter 13 Introduction

pytest enables test parametrization at several levels:
• pytest.fixture() allows one to parametrize fixture functions.
• @pytest.mark.parametrize allows one to define multiple sets of arguments and fixtures at the test function or
class.
• pytest_generate_tests allows one to define custom parametrization schemes or extensions.


## 13.1 @pytest.mark.parametrize: parametrizing test functions

The builtin pytest.mark.parametrize decorator enables parametrization of arguments for a test function. Here is a
typical example of a test function that implements checking that a certain input leads to an expected output:
```python
# content of test_expectation.py
import pytest
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
assert eval(test_input) == expected
```
Here, the @parametrize decorator defines three different (test_input,expected) tuples so that the
test_eval function will run three times using them in turn:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 3 items
test_expectation.py ..F [100%]
================================= FAILURES =================================
____________________________ test_eval[6*9-42] _____________________________
test_input = '6*9', expected = 42
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9",
˓→42)])
def test_eval(test_input, expected):
> assert eval(test_input) == expected
E AssertionError: assert 54 == 42
E + where 54 = eval('6*9')
test_expectation.py:6: AssertionError
==================== 1 failed, 2 passed in 0.12 seconds ====================
```
Note: pytest by default escapes any non-ascii characters used in unicode strings for the parametrization because it has
several downsides. If however you would like to use unicode strings in parametrization and see them in the terminal
as is (non-escaped), use this option in your pytest.ini:
```
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True
```
Keep in mind however that this might cause unwanted side effects and even bugs depending on the OS used and
plugins currently installed, so use it at your own risk.
<br>
As designed in this example, only one pair of input/output values fails the simple test function. And as usual with test
function arguments, you can see the input and output values in the traceback.
Note that you could also use the parametrize marker on a class or a module (see Marking test functions with attributes)
which would invoke several functions with the argument sets.
It is also possible to mark individual test instances within parametrize, for example with the builtin mark.xfail:
```python
# content of test_expectation.py
import pytest
@pytest.mark.parametrize(
"test_input,expected",
[("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
assert eval(test_input) == expected
```
Let’s run this:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 3 items
test_expectation.py ..x [100%]
=================== 2 passed, 1 xfailed in 0.12 seconds ====================
```
The one parameter set which caused a failure previously now shows up as an “xfailed (expected to fail)” test.
In case the values provided to parametrize result in an empty list - for example, if they’re dynamically generated
by some function - the behaviour of pytest is defined by the empty_parameter_set_mark option.
To get all combinations of multiple parametrized arguments you can stack parametrize decorators:
```python
import pytest
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
pass
```
This will run the test with the arguments set to x=0/y=2, x=1/y=2, x=0/y=3, and x=1/y=3 exhausting parameters in the order of the decorators.### 12.1.1 skipif

## 13.2 Basic pytest_generate_tests example

Sometimes you may want to implement your own parametrization scheme or implement some dynamism for determining the parameters or scope of a fixture. For this, you can use the pytest_generate_tests hook which is
called when collecting a test function. Through the passed in metafunc object you can inspect the requesting test
context and, most importantly, you can call metafunc.parametrize() to cause parametrization.

For example, let’s say we want to run a test taking string inputs which we want to set via a new pytest command
line option. Let’s first write a simple test accepting a stringinput fixture function argument:
```python
# content of test_strings.py
def test_valid_string(stringinput):
assert stringinput.isalpha()
```
Now we add a conftest.py file containing the addition of a command line option and the parametrization of our
test function:
```python
# content of conftest.py
def pytest_addoption(parser):
parser.addoption(
"--stringinput",
action="append",
default=[],
help="list of stringinputs to pass to test functions",
)
def pytest_generate_tests(metafunc):
if "stringinput" in metafunc.fixturenames:
metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))
```
If we now pass two stringinput values, our test will run twice:
```
$ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
.. [100%]
2 passed in 0.12 seconds
```
Let’s also run with a stringinput that will lead to a failing test:
```
$ pytest -q --stringinput="!" test_strings.py
F [100%]
================================= FAILURES =================================
___________________________ test_valid_string[!] ___________________________
stringinput = '!'
def test_valid_string(stringinput):
> assert stringinput.isalpha()
E AssertionError: assert False
E + where False = <built-in method isalpha of str object at 0xdeadbeef>()
E + where <built-in method isalpha of str object at 0xdeadbeef> = '!'.
˓→isalpha
test_strings.py:4: AssertionError
1 failed in 0.12 seconds
```
As expected our test function fails.
If you don’t specify a stringinput it will be skipped because metafunc.parametrize() will be called with an
empty parameter list:
```
$ pytest -q -rs test_strings.py
s [100%]
========================= short test summary info ==========================
SKIPPED [1] test_strings.py: got empty parameter set ['stringinput'], function test_
˓→valid_string at $REGENDOC_TMPDIR/test_strings.py:2
1 skipped in 0.12 seconds
```
Note that when calling metafunc.parametrize multiple times with different parameter sets, all parameter names
across those sets cannot be duplicated, otherwise an error will be raised.
## 13.3 More examples
For further examples, you might want to look at more parametrization examples.
