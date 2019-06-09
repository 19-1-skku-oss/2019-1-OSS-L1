---
layout: post
title: Getting Started-Pytest
summary: Chapter 1
featured-img: children
---


# Installation and Getting Started

Pythons: Python 2.7, 3.4, 3.5, 3.6, 3.7, Jython, PyPy-2.3

Platforms: Unix/Posix and Windows

PyPI package name: pytest

Documentation as PDF: [download latest](https://docs.pytest.org/en/latest/contents.html)

pytest is a framework that makes building simple and scalable tests easy. Tests are expressive and readable—no
boilerplate code required. Get started in minutes with a small unit test or complex functional test for your application
or library.
<br>

1.1 Install pytest
---
1. Run the following command in your command line:
```
pip install -U pytest
```
2. Check that you installed the correct version:
```
$ pytest --version
This is pytest version 4.x.y, imported from $PYTHON_PREFIX/lib/python3.6/site-
˓→packages/pytest.py
```
<br>

1.2 Create your first test
---
Create a simple test function with just four lines of code:
```python
# content of test_sample.py
def func(x):
	return x + 1
def test_answer():
	assert func(3) == 5
```
That’s it. You can now execute the test function:
```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item
test_sample.py F						 [100%]
================================= FAILURES =================================
_______________________________ test_answer ________________________________

	def test_answer():
> 		assert func(3) == 5
E 		assert 4 == 5
E 		+ where 4 = func(3)

test_sample.py:5: AssertionError
========================= 1 failed in 0.12 seconds =========================
```
This test returns a failure report because func(3) does not return 5.

>Note: You can use the assert statement to verify test expectations. pytest’s [Advanced assertion introspection](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) will intelligently report intermediate values of the assert expression so you can avoid the many names of [JUnit legacy methods](https://docs.python.org/3/library/unittest.html#test-cases)
<br>

1.3 Run multiple tests
---
pytest will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories. More
generally, it follows [standard test discovery rules]("chapter_23.2").
<br><br>

1.4 Assert that a certain exception is raised
---
Use the [raises]("chapter_4.2") helper to assert that some code raises an exception:
```python
# content of test_sysexit.py
import pytest
def f():
	raise SystemExit(1)
def test_mytest():
	with pytest.raises(SystemExit):
		f()
```
Execute the test function with “quiet” reporting mode:
```
$ pytest -q test_sysexit.py
. 								[100%]
1 passed in 0.12 seconds
```
<br>

1.5 Group multiple tests in a class
---
Once you develop multiple tests, you may want to group them into a class. pytest makes it easy to create a class
containing more than one test:
```python
# content of test_class.py
class TestClass(object):
	def test_one(self):
		x = "this"
		assert 'h' in x
        
	def test_two(self):
		x = "hello"
		assert hasattr(x, 'check')
```
pytest discovers all tests following its [Conventions for Python test discovery]("chapter_23.2"), so it finds both test_ prefixed
```
$ pytest -q test_class.py
.F 								[100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________
self = <test_class.TestClass object at 0xdeadbeef>

	def test_two(self):
		x = "hello"
> 		assert hasattr(x, 'check')
E 		AssertionError: assert False
E 	    +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
1 failed, 1 passed in 0.12 seconds
```
The first test passed and the second failed. You can easily see the intermediate values in the assertion to help you
understand the reason for the failure.
<br>

1.6 Request a unique temporary directory for functional tests
---
pytest provides [Builtin fixtures/function arguments](https://docs.pytest.org/en/latest/builtin.html#builtinfixtures) to request arbitrary resources, like a unique temporary directory:
```python
# content of test_tmpdir.py
def test_needsfiles(tmpdir):
	print(tmpdir)
	assert 0
```
List the name tmpdir in the test function signature and pytest will lookup and call a fixture factory to create the
resource before performing the test function call. Before the test runs, pytest creates a unique-per-test-invocation
temporary directory:
```
$ pytest -q test_tmpdir.py
F 								[100%]
================================= FAILURES =================================
_____________________________ test_needsfiles ______________________________
tmpdir = local('PYTEST_TMPDIR/test_needsfiles0')

	def test_needsfiles(tmpdir):
		print(tmpdir)
> 		assert 0
E 		assert 0

test_tmpdir.py:3: AssertionError
--------------------------- Captured stdout call ---------------------------
PYTEST_TMPDIR/test_needsfiles0
1 failed in 0.12 seconds
```
More info on `tmpdir` handling is available at [Temporary directories and files]("chapter_8").
Find out what kind of builtin [pytest fixtures] exist with the command:
```
pytest --fixtures 	# shows builtin and custom fixtures
```
Note that this command omits fixtures with leading _ unless the `-v` option is added
<br>


1.7 Continue reading
---
Check out additional pytest resources to help you customize tests for your unique workflow:
- “[Calling pytest through python -m pytest]("chapter_2”)” for command line invocation examples
- “[Using pytest with an existing test suite("chapter_3")]" for working with pre-existing tests
- “[Marking test functions with attributes]("chapter_6")” for information on the pytest.mark mechanism
- “[pytest fixtures: explicit, modular, scalable]("chapter_5")” for providing a functional baseline to your tests
- “[Writing plugins]("chapter_19")” for managing and writing plugins
- “[Good Integration Practices]("chapter_23")” for virtualenv and test layouts



