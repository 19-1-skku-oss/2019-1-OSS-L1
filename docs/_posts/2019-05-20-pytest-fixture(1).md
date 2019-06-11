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
smtp_connection. A matching fixture function is discovered by looking for a fixture-marked function
named smtp_connection.
2. smtp_connection() is called to create an instance.
3. test_ehlo(<smtp_connection instance>) is called and fails in the last line of the test function.
Note that if you misspell a function argument or want to use one that isn’t available, you’ll see an error with a list of
available function arguments.

매개 변수의 철자를 잘못 입력했거나 사용할 수 없는 것을 사용하려는 경우 `smtp_connection` 이라는 사용 가능한 매개 변수 목록에 오류가 표시됩니다.

---
사용할 수 있는 fixture를 보기 위해서는 아래와 같이 하십시오.
```
pytest --fixtures test_simplefactory.py
```
-v 옵션을 입력하면 fixture 이름 앞의 _ 가 무시됩니다.

---


fixture: dependency injection의 대표적인 예
---
fixture를 통해 가져오기, 설정, 정리 등 세부사항을 신경쓰지 않고도 사전에 초기화된 특정 응용 프로그램 객체를 쉽게 받아 작업할 수 있습니다. fixture 함수가 injector 역할을 하고 테스트 함수가 fixture 객체의 소비자인 대표적인 [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)의 예 입니다.
<br>

`conftest.py`: ficture 함수의 공유
---
테스트를 구현하는 동안 여러 테스트 파일의 fixture 함수를 사용하려는 경우 이를 `conftest.py` 파일로 옮길 수 있습니다. 테스트에 사용할 fixture 함수를 가져 올 필요가 없으며, 자동으로 `pytest`에 의해 발견됩니다. Fixture 함수의 발견은 테스트 class, 테스트 모듈, 그리고 `conftest.py` 파일 그리고 마지막으로 내장 플러그인과 third-party 플러그인 순으로 진행됩니다.
또한, [local per-directory plugins]("chapter_19.2")를 사용하여 'conftest.py' 를 구현할 수 있습니다.
<br>

테스트 정보의 공유
---
파일에서 테스트 정보를 테스트에 사용할 수 있게 하려면, 이 정보를 테스트에서 사용할 수 있도록 fixture에 load해야 합니다. 이것은 pytest의 자동 캐싱 메커니즘을 사용합니다.
또 다른 좋은 방법은 테스트 폴더에 데이터 파일을 추가 하는 것 입니다. 이러한 방식에 도움이 되는 커뮤니티 플러그인이 있습니다.(예: pytest-datadir 및 pytest-datafile)
<br>

범위: class, 모듈, session 내부에서의 fixture 객체의 공유
---
네트워크 연결이 필요한 fixture는 연결성에 달려 있으며 대개 시간이 많이 소요됩니다. 앞의 예제를 확장하면 `@pytest.fixture` 호출에 scope="modlue" 매개 변수를 추가하여 smtp_connection fixture 함수가 테스트 모듈당 한 번만 호출되도록 할 수 있습니다.(기본 값은 테스트 함수 당 한번 호출하는 것 입니다.) 테스트 모듈의 여러 테스트 기능은 각각 동일한 `smtp_connection` fixture 인스턴스를 수신하므로 시간이 절약됩니다. 범위로 사용할 수 있는 값은 fucntion, class, module, package, 또는 session 입니다.
다음 예제는 fixture 함수를 별도의 conftest.py 파일에 저장하여 디렉토리에 있는 여러 테스트 모듈의 테스트가 fixture 함수에 접근 할 수 있도록합니다.
```python
# content of conftest.py
import pytest
import smtplib

@pytest.fixture(scope="module")
def smtp_connection():
	return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
```
fixture의 이름은 `smtp_connection`이며, 테스트 또는 conftest.py가 있는 디렉토리 혹은 그 하위 디렉토리에 있는 fixture 함수에 `smtp_connection`이라는 이름을 입력 매개 변수로 나열하여 결과에 접근 할 수 있습니다.
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
우리는 무슨 일이 일어나고 있는지 검사하기 위해 실패할 assert 0 문을 삽입하고 테스트를 진행합니다.
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
위의 결과를 확인함으로써 동일한 smtp_connection 객체가 두개의 테스트 함수로 전달되었음을 볼 수 있습니다. 결과적으로 smtp_connection을 사용하는 두 테스트 함수는 동일한 인스턴스를 다시 사용하기 때문에 단일 테스트만큼 빠르게 실행됩니다.
세션 범위로 지정된 smtp_connection 인스턴스를 갖고 싶다면 간단히 선언하면 됩니다.
```
@pytest.fixture(scope="session")
def smtp_connection():
	# the returned fixture value will be shared for
	# all tests needing it
	...
```
마지막으로, `class` 범위는 test class가 실해될때 마다 실행됩니다.

---
주의: pytest는 한번에 하나의 fixture만 캐시합니다. 즉, 매개 변수화 된 fixture를 사용할 때 pytest는 주어진 범위 내에서 fixture를 두 번 이상 호출할 수 있습니다.

---

상위 범위의 fixture가 먼저 인스턴스화
---
feature에 대한 함수의 요청에서, 상위 범위(예: session)의 fixture는 함수 또는 class와 같은 낮은 범위의 fixture보다 먼저 인스턴스화됩니다. 동일한 범위의 fixture의 상대적 순서는 테스트 함수에서 선언 된 순서를 따르고 fixture들 사이의 의존성을 존중합니다.
아래의 코드를 살펴봅시다.
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

test_foo에 의해 요청된 fixture는 다음과 같은 순서로 인스턴스화 됩니다.
- `s1`: 제일 상위 범위의 fixture(session)
- `m1`: 두번째로 높은 범위의 fixture(module)
- `tmpdir`: f1에 의해 요청되는 함수 범위의 fixture, `f1`에 의해 사용되기 때문에 이 시점에서 인스턴스화 되어야 합니다.
- `f1`: `test_foo`의 첫번째 매개 변수인 function 범위의 fixture
- `f2`: `test_foo`의 마지막 매개 변수인 function 범위의 fixture
