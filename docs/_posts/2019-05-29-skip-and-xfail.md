---
layout: post
title: "Skip and xfail: dealing with tests that cannot succeed"
summary: Chapter 12
featured-img: temp
---
## Chapter 12 Summary

You can mark test functions that cannot be run on certain platforms or that you expect to fail so pytest can deal with
them accordingly and present a summary of the test session, while keeping the test suite green.
A skip means that you expect your test to pass only if some conditions are met, otherwise pytest should skip running
the test altogether. Common examples are skipping windows-only tests on non-windows platforms, or skipping tests
that depend on an external resource which is not available at the moment (for example a database).
A xfail means that you expect a test to fail for some reason. A common example is a test for a feature not yet
implemented, or a bug not yet fixed. When a test passes despite being expected to fail (marked with pytest.mark.
xfail), it’s an xpass and will be reported in the test summary.
pytest counts and lists skip and xfail tests separately. Detailed information about skipped/xfailed tests is not shown
by default to avoid cluttering the output. You can use the -r option to see details corresponding to the “short” letters
shown in the test progress:
```
pytest -rxXs # show extra info on xfailed, xpassed, and skipped tests
```
More details on the -r option can be found by running pytest -h.


## 12.1 Skipping test functions

The simplest way to skip a test function is to mark it with the skip decorator which may be passed an optional
reason:
```python
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
...
```
Alternatively, it is also possible to skip imperatively during test execution or setup by calling the pytest.
skip(reason) function:
```python
def test_function():
if not valid_config():
pytest.skip("unsupported configuration")
```
The imperative method is useful when it is not possible to evaluate the skip condition during import time.
It is also possible to skip the whole module using pytest.skip(reason, allow_module_level=True)
at the module level:
```python
import sys
import pytest
if not sys.platform.startswith("win"):
pytest.skip("skipping windows-only tests", allow_module_level=True)
```
## 8.2 The tmp_path_factory fixture
tmp_path_factory는 다른 테스트나 fixture로 부터 임의적인 임시 주소를 만드는데 사용되는 fixture입니다.
이것은 tmpdir_factory를 다른 곳에 위치 시키고,  pathlib.Path instances 반환하게 하기 위함입니다.

```python
# contents of conftest.py

import pytest
@pytest.fixture(scope="session")
  def image_file(tmpdir_factory):
      img = compute_expensive_image()
      fn = tmpdir_factory.mktemp("data").join("img.png")
      img.save(str(fn))
      return fn
# contents of test_image.py
def test_histogram(image_file):
    img = load_image(image_file)
    # compute and test histogram

```

### 12.1.1 skipif

If you wish to skip something conditionally then you can use skipif instead. Here is an example of marking a test
function to be skipped when run on an interpreter earlier than Python3.6:
```python
import sys
@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_function():
...
```
If the condition evaluates to True during collection, the test function will be skipped, with the specified reason
appearing in the summary when using -rs.

You can share skipif markers between modules. Consider this test module:
```python
# content of test_mymodule.py
import mymodule
minversion = pytest.mark.skipif(
mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
)
@minversion
def test_function():
...
```
You can import the marker and reuse it in another test module:
```python
# test_myothermodule.py
from test_mymodule import minversion
@minversion
def test_anotherfunction():
...
```
For larger test suites it’s usually a good idea to have one file where you define the markers which you then consistently
apply throughout your test suite.
Alternatively, you can use condition strings instead of booleans, but they can’t be shared between modules easily so
they are supported mainly for backward compatibility reasons.
Reference: pytest.mark.skipif

### 12.1.2 Skip all test functions of a class or module
You can use the skipif marker (as any other marker) on classes:
```python
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls(object):
def test_function(self):
"will not be setup or run under 'win32' platform"
```
If the condition is True, this marker will produce a skip result for each of the test methods of that class.
If you want to skip all test functions of a module, you may use the pytestmark name on the global level:
```python
# test_module.py
pytestmark = pytest.mark.skipif(...)
```
If multiple skipif decorators are applied to a test function, it will be skipped if any of the skip conditions is true.

### 12.1.3 Skipping files or directories
Sometimes you may need to skip an entire file or directory, for example if the tests rely on Python version-specific
features or contain code that you do not wish pytest to run. In this case, you must exclude the files and directories
from collection. Refer to Customizing test collection for more information.

### 12.1.4 Skipping on a missing import dependency
You can use the following helper at module level or within a test or test setup function:
```python
docutils = pytest.importorskip("docutils")
```
If docutils cannot be imported here, this will lead to a skip outcome of the test. You can also skip based on the
version number of a library:
```python
docutils = pytest.importorskip("docutils", minversion="0.3")
```
The version will be read from the specified module’s __version__ attribute.
### 12.1.5 Summary
Here’s a quick guide on how to skip tests in a module in different situations:
1. Skip all tests in a module unconditionally:
```python
pytestmark = pytest.mark.skip("all tests still WIP")
```
2. Skip all tests in a module based on some condition:
```python
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for
˓→linux only")
```
3. Skip all tests in a module if some import is missing:
```python
pexpect = pytest.importorskip("pexpect")
```
## 12.2 XFail: mark test functions as expected to fail
You can use the xfail marker to indicate that you expect a test to fail:
```python
@pytest.mark.xfail
def test_function():
...
```
This test will be run but no traceback will be reported when it fails. Instead terminal reporting will list it in the
“expected to fail” (XFAIL) or “unexpectedly passing” (XPASS) sections.
Alternatively, you can also mark a test as XFAIL from within a test or setup function imperatively:
```python
def test_function():
if not valid_config():
pytest.xfail("failing configuration (but should work)")
```
This will unconditionally make test_function XFAIL. Note that no other code is executed after pytest.
xfail call, differently from the marker. That’s because it is implemented internally by raising a known exception.
Reference: pytest.mark.xfail

### 12.2.1 strict parameter
Both XFAIL and XPASS don’t fail the test suite, unless the strict keyword-only parameter is passed as True:
```python
@pytest.mark.xfail(strict=True)
def test_function():
...
```
This will make XPASS (“unexpectedly passing”) results from this test to fail the test suite.
You can change the default value of the strict parameter using the xfail_strict ini option:
```
[pytest]
xfail_strict=true
```

### 12.2.2 reason parameter
As with skipif you can also mark your expectation of a failure on a particular platform:
```python
@pytest.mark.xfail(sys.version_info >= (3, 6), reason="python3.6 api changes")
def test_function():
...
```
### 12.2.3 raises parameter
If you want to be more specific as to why the test is failing, you can specify a single exception, or a tuple of exceptions,
in the raises argument.
```python
@pytest.mark.xfail(raises=RuntimeError)
def test_function():
...
```
Then the test will be reported as a regular failure if it fails with an exception not mentioned in raises.
### 12.2.4 run parameter
If a test should be marked as xfail and reported as such but should not be even executed, use the run parameter as
False:
```python
@pytest.mark.xfail(run=False)
def test_function():
...
```
This is specially useful for xfailing tests that are crashing the interpreter and should be investigated later.
### 12.2.5 Ignoring xfail
By specifying on the commandline:
```
pytest --runxfail
```
you can force the running and reporting of an xfail marked test as if it weren’t marked at all. This also causes
pytest.xfail to produce no effect.
### 12.2.6 Examples
Here is a simple test file with the several usages:
```python
import pytest
xfail = pytest.mark.xfail
@xfail
def test_hello():
assert 0
@xfail(run=False)
def test_hello2():
assert 0
@xfail("hasattr(os, 'sep')")
def test_hello3():
assert 0
(continues on next page)
12.2. XFail: mark test functions as expected to fail 81
pytest Documentation, Release 4.6
(continued from previous page)
@xfail(reason="bug 110")
def test_hello4():
assert 0
@xfail('pytest.__version__[0] != "17"')
def test_hello5():
assert 0
def test_hello6():
pytest.xfail("reason")
@xfail(raises=IndexError)
def test_hello7():
x = []
x[1] = 1
```
Running it with the report-on-xfail option gives this output:
```
example $ pytest -rx xfail_demo.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR/example
collected 7 items
xfail_demo.py xxxxxxx [100%]
========================= short test summary info ==========================
XFAIL xfail_demo.py::test_hello
XFAIL xfail_demo.py::test_hello2
reason: [NOTRUN]
XFAIL xfail_demo.py::test_hello3
condition: hasattr(os, 'sep')
XFAIL xfail_demo.py::test_hello4
bug 110
XFAIL xfail_demo.py::test_hello5
condition: pytest.__version__[0] != "17"
XFAIL xfail_demo.py::test_hello6
reason: reason
XFAIL xfail_demo.py::test_hello7
======================== 7 xfailed in 0.12 seconds =========================
```
## 12.3 Skip/xfail with parametrize
It is possible to apply markers like skip and xfail to individual test instances when using parametrize:
```python
import pytest
(continues on next page)
82 Chapter 12. Skip and xfail: dealing with tests that cannot succeed
pytest Documentation, Release 4.6
(continued from previous page)
@pytest.mark.parametrize(
("n", "expected"),
[
(1, 2),
pytest.param(1, 0, marks=pytest.mark.xfail),
pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
(2, 3),
(3, 4),
(4, 5),
pytest.param(
10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k
˓→")
),
],
)
def test_increment(n, expected):
assert n + 1 == expected
```
