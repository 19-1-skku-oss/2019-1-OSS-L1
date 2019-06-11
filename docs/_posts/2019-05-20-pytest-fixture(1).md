---
layout: post
title: Pytest fixture(1)
summary: Chapter 5-1
featured-img: code
---
# pytest fixtures: explicit, modular, scalable

The [purpose of test fixtures](https://en.wikipedia.org/wiki/Test_fixture#Software) is to provide a fixed baseline upon which tests can reliably and repeatedly execute. pytest
fixtures offer dramatic improvements over the classic xUnit style of setup/teardown functions:
• fixtures have explicit names and are activated by declaring their use from test functions, modules, classes or
whole projects.
• fixtures are implemented in a modular manner, as each fixture name triggers a fixture function which can itself
use other fixtures.
• fixture management scales from simple unit to complex functional testing, allowing to parametrize fixtures and
tests according to configuration and component options, or to re-use fixtures across function, class, module or
whole test session scopes.
In addition, pytest continues to support [classic xunit-style setup]("chapter_17"). You can mix both styles, moving incrementally from classic to new style, as you prefer. You can also start out from existing [unittest.TestCase]("chapter_15") style or [nose based]("chapter_16") projects.


5.1 Fixtures as Function arguments
---
Test functions can receive fixture objects by naming them as an input argument. For each argument name, a fixture
function with that name provides the fixture object. Fixture functions are registered by marking them with `@pytest.
fixture`. Let’s look at a simple self-contained test module containing a fixture and a test function using it:
```python
# content of ./test_smtpsimple.py
import pytest

@pytest.fixture
def smtp_connection():
	import smtplib
	return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
def test_ehlo(smtp_connection):
	response, msg = smtp_connection.ehlo()
	assert response == 250
	assert 0 # for demo purposes
```

Here, the `test_ehlo` needs the `smtp_connection` fixture value. pytest will discover and call the `@pytest.
fixture` marked `smtp_connection` fixture function. Running the test looks like this:
```
$ pytest test_smtpsimple.py
======================== test session starts =========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item

test_smtpsimple.py F 							[100%]

============================== FAILURES ==============================
_____________________________ test_ehlo ______________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_ehlo(smtp_connection):
		response, msg = smtp_connection.ehlo()
		assert response == 250
> 		assert 0 # for demo purposes
E 		assert 0

test_smtpsimple.py:11: AssertionError
====================== 1 failed in 0.12 seconds ======================
```

In the failure traceback we see that the test function was called with a `smtp_connection` argument, the `smtplib.
SMTP()` instance created by the fixture function. The test function fails on our deliberate assert 0. Here is the
exact protocol used by `pytest` to call the test function this way:

1. pytest finds the `test_ehlo` because of the test_ prefix. The test function needs a function argument named
`smtp_connection`. A matching fixture function is discovered by looking for a fixture-marked function
named `smtp_connection`.
2. `smtp_connection()` is called to create an instance.
3. `test_ehlo`(`<smtp_connection instance>`) is called and fails in the last line of the test function.
Note that if you misspell a function argument or want to use one that isn’t available, you’ll see an error with a list of
available function arguments.

---
Note: You can always issue:
```
pytest --fixtures test_simplefactory.py
```
to see available fixtures (fixtures with leading _ are only shown if you add the -v option).

---


5.2 Fixtures: a prime example of dependency injection
---
Fixtures allow test functions to easily receive and work against specific pre-initialized application objects without
having to care about import/setup/cleanup details. It’s a prime example of [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) where fixture functions take the role of the injector and test functions are the consumers of fixture objects.

<br>

5.3 `conftest.py`: sharing fixture functions
---
If during implementing your tests you realize that you want to use a fixture function from multiple test files you can
move it to a `conftest.py` file. You don’t need to import the fixture you want to use in a test, it automatically gets
discovered by pytest. The discovery of fixture functions starts at test classes, then test modules, then `conftest.py`
files and finally builtin and third party plugins.
You can also use the `conftest.py` file to implement [local per-directory plugins]("chapter_19.2").

<br>

5.4 Sharing test data
---
If you want to make test data from files available to your tests, a good way to do this is by loading these data in a
fixture for use by your tests. This makes use of the automatic caching mechanisms of pytest.
Another good approach is by adding the data files in the tests folder. There are also community plugins available
to help managing this aspect of testing, e.g. pytest-datadir and pytest-datafiles.
<br>

5.5 Scope: sharing a fixture instance across tests in a class, moduleor session
---
Fixtures requiring network access depend on connectivity and are usually time-expensive to create. Extending the
previous example, we can add a `scope="module"` parameter to the `@pytest.fixture` invocation to cause the
decorated `smtp_connection` fixture function to only be invoked once per test module (the default is to invoke once
per test function). Multiple test functions in a test module will thus each receive the same `smtp_connection` fixture
instance, thus saving time. Possible values for `scope` are: `function`, `class`, `module`, `package` or `session`.
The next example puts the fixture function into a separate `conftest.py` file so that tests from multiple test modules
in the directory can access the fixture function:
```python
# content of conftest.py
import pytest
import smtplib

@pytest.fixture(scope="module")
def smtp_connection():
	return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
```
The name of the fixture again is `smtp_connection` and you can access its result by listing the name
`smtp_connection` as an input parameter in any test or fixture function (in or below the directory where `conftest.py` is located):
```python
# content of test_module.py

def test_ehlo(smtp_connection):
	response, msg = smtp_connection.ehlo()
	assert response == 250
	assert b"smtp.gmail.com" in msg
	assert 0 # for demo purposes
```
<br>
```python
def test_noop(smtp_connection):
	response, msg = smtp_connection.noop()
	assert response == 250
	assert 0 # for demo purposes
```
We deliberately insert failing `assert 0` statements in order to inspect what is going on and can now run the tests:
```
$ pytest test_module.py
========================= test session starts ==========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 2 items

test_module.py FF 							[100%]

=============================== FAILURES ===============================
______________________________ test_ehlo _______________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_ehlo(smtp_connection):
		response, msg = smtp_connection.ehlo()
		assert response == 250
		assert b"smtp.gmail.com" in msg
> 		assert 0 # for demo purposes
E 		assert 0
	test_module.py:6: AssertionError
______________________________ test_noop _______________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_noop(smtp_connection):
		response, msg = smtp_connection.noop()
		assert response == 250
> 		assert 0 # for demo purposes
E 		assert 0

test_module.py:11: AssertionError
======================= 2 failed in 0.12 seconds =======================
```
You see the two `assert 0` failing and more importantly you can also see that the same (module-scoped)
`smtp_connection` object was passed into the two test functions because pytest shows the incoming argument
values in the traceback. As a result, the two test functions using `smtp_connection` run as quick as a single one
because they reuse the same instance.
If you decide that you rather want to have a session-scoped `smtp_connection` instance, you can simply declare it:
```
@pytest.fixture(scope="session")
def smtp_connection():
	# the returned fixture value will be shared for
	# all tests needing it
	...
```
Finally, the `class` scope will invoke the fixture once per test class.

---
Note: Pytest will only cache one instance of a fixture at a time. This means that when using a parametrized fixture,
pytest may invoke a fixture more than once in the given scope.

---

5.6 Higher-scoped fixtures are instantiated first
---
Within a function request for features, fixture of higher-scopes (such as `session`) are instantiated first than lowerscoped fixtures (such as `function` or `class`). The relative order of fixtures of same scope follows the declared
order in the test function and honours dependencies between fixtures.
Consider the code below:
```python
@pytest.fixture(scope="session")
def s1():
	pass

@pytest.fixture(scope="module")
def m1():
	pass

@pytest.fixture
def f1(tmpdir):
	pass

@pytest.fixture
def f2():
	pass

def test_foo(f1, m1, f2, s1):
	...
```

The fixtures requested by `test_foo` will be instantiated in the following order:
- `s1`:  is the highest-scoped fixture (`session`).
- `m1`:  is the second highest-scoped fixture (`module`).
- `tmpdir`:  is a `function`-scoped fixture, required by `f1`: it needs to be instantiated at this point because it is
a dependency of `f1`.
- `f1`: is the first `function`-scoped fixture in `test_foo` parameter list
- `f2`:  is the last `function`-scoped fixture in `test_foo` parameter list.
