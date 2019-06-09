---
title: "사용법 그리고 실행방법(1)"
date: 2019-06-04 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---

Terminal command로 python을 이용하더라도, -m 옵션 flag를 통해 pytest를 실행할 수 있습니다.
: python -m pytest

python -m pytest가 현재 위치의 directory를 sys.path에 저장한다는 사실 이외에는 사실상 pytest 명령어와 다를 것이 없습니다.

## 가능한 종료 상황(exit codes)들은 총 6가지 경우가 있습니다.

모든 테스트들이 성공적으로 모여지고 통과된 경우, Exit code 0

테스트들이 모여지고, 실행되어졌지만 부분적으로 실패한 경우, Exit code 1

유저에 의해 Test가 중지된 경우, Exit code 2

테스트 실행 중 내부 에러가 발생한 경우, Exit code 3

Terminal 상의 pytest command line 사용법에 error가 생긴 경우, Exit code 4

단 하나의 테스트도 모이지 않은 경우, Exit code 5

## 버젼, 옵션 flag 이름들, 그리고 환경변수들에 관한 정보들

```
pytest --version   # shows where pytest was imported from
pytest --fixtures  # show available builtin function arguments
pytest -h | --help # show help on command line and config file options
```

처음 실패 후 멈추거나, (N)회 실패 후 멈추게 하는 방법들
-x(1회) --maxfail=2(2회,-> N회 가능)

```
pytest -x            # stop after first failure
pytest --maxfail=2    # stop after two failures
Specifying tests / selecting tests
Pytest supports several ways to run and select tests from the command-line.
```

## 모듈 상에 있는 테스트 실행하기

```
pytest test_mod.py
```
directory 내에 있는 테스트들 실행하기

pytest testing/
키워드 표현법에 따라 테스트들 실행하기<br>

pytest -k "MyClass and not method"
테스트 중에 주어진 문자열을 포함한 테스트들을 실행하기<br>

Run tests by node ids

노드 ID로 테스트 실행하기 ::로 구분시켜서 실행

모듈 내에서 특정한 테스트를 실행하려면, 아래와 같이 실행하면 됩니다.

```
pytest test_mod.py::test_func
```
Another example specifying a test method in the command line:

```
pytest test_mod.py::TestClass::test_method
```
마커 표현법으로 테스트들 실행하기

pytest -m slow
@pytest.mark.slow decorator를 활용해서 모든 테스트들을 실행하기

For more information see marks.

## packages들로부터 테스트들 실행하기

pytest --pyargs pkg.testing
위의 방법으로 pkg.testing을 들여와 그것의 filesystem 상 위치를 찾고, pkg.testing에서 들어온 테스트들을 실행시킵니다.

Python 흔적 출력방식 수정하기

Examples for modifying traceback printing:
```
pytest --showlocals # show local variables in tracebacks
pytest -l           # show local variables (shortcut)

pytest --tb=auto    # (default) 'long' tracebacks for the first and last
                     # entry, but 'short' style for the other entries
pytest --tb=long    # exhaustive, informative traceback formatting
pytest --tb=short   # shorter traceback format
pytest --tb=line    # only one line per failure
pytest --tb=native  # Python standard library formatting
pytest --tb=no      # no traceback at all
```

--full-trace는 error에 대해 매우긴 흔적을 남깁니다. --tb=long 옵션과 비교해봐도 깁니다. 또한 --full-trace는 (Ctrl+C)에 따른 stack trace도 출력시킵니다. 이것은 매우 유용한데, 테스트들을 실행하는데 너무 오래 걸려 (Ctrl+C)로 정지 Interrupt 시켰을 경우, 어디 test들에 머물러 있는지 확인할 수 있습니다. 기본값으로는 어떠한 출력값도 나오지 않습니다. 왜냐하면 KeyboardInterrupt이 pytest에 잡혔기 때문이죠. 이러한 옵션을 사용하는 것으로, 흔적을 보이게 할 수 있습니다.

Detailed summary report
-r flag는 "short test summary info' 정보를 테스트 세션 끝에 보이게 하는데 쓸 수 있습니다. 아주 큰 테스트들에 대해서, 모든 실패, 넘긴 상황들을 파악하는데 도움이 됩니다.


Example:

```
# content of test_example.py
import pytest


@pytest.fixture
def error_fixture():
    assert 0


def test_ok():
    print("ok")


def test_fail():
    assert 0


def test_error(error_fixture):
    pass


def test_skip():
    pytest.skip("skipping this test")


def test_xfail():
    pytest.xfail("xfailing this test")


@pytest.mark.xfail(reason="always xfail")
def test_xpass():
    pass
$ pytest -ra
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
========================= short test summary info ==========================
SKIPPED [1] $REGENDOC_TMPDIR/test_example.py:23: skipping this test
XFAIL test_example.py::test_xfail
  reason: xfailing this test
XPASS test_example.py::test_xpass always xfail
ERROR test_example.py::test_error - assert 0
FAILED test_example.py::test_fail - assert 0
= 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12 seconds =
The -r options accepts a number of characters after it, with a used above meaning “all except passes”.

Here is the full list of available characters that can be used:

f - failed
E - error
s - skipped
x - xfailed
X - xpassed
p - passed
P - passed with output
a - all except pP
A - all
More than one character can be used, so for example to only see failed and skipped tests, you can execute:

$ pytest -rfs
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
========================= short test summary info ==========================
FAILED test_example.py::test_fail - assert 0
SKIPPED [1] $REGENDOC_TMPDIR/test_example.py:23: skipping this test
= 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12 seconds =
Using p lists the passing tests, whilst P adds an extra section “PASSES” with those tests that passed but had captured output:

$ pytest -rpP
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
================================== PASSES ==================================
_________________________________ test_ok __________________________________
--------------------------- Captured stdout call ---------------------------
ok
========================= short test summary info ==========================
PASSED test_example.py::test_ok
= 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12 seconds =
```
