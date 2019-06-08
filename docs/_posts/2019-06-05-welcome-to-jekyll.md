---
layout: post
---
# 사용법 그리고 실행방법

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

## For more information see marks.

packages들로부터 테스트들 실행하기

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

## Dropping to PDB (Python Debugger) on failures
Python은 PDB라 불리는 내장된 Python debugger와 같이 설치됩니다. pytest는 아래와 같은 command line 상 명령어를 통해 PDB prompt로 들어갑니다.

```
pytest --pdb
```
위의 명령어는 모든 실패에 대해 Python debugger를 실행시킵니다. 종종 오로지 첫번째 실패에 대해서만 실패 상황을 이해하기 위해 이 작업을 원하기도 하는데, 그런 경우, 아래와 같이 실행시키면 됩니다.

```
pytest -x --pdb   # drop to PDB on first failure, then end test session
pytest --pdb --maxfail=3  # drop to PDB for first three failures
```
어떠한 실패상황에 대해서도 관련 예외정보가 sys.last_value, sys.last_type and sys.last_traceback 에 저장됩니다. 양방향 사용 관점에서는 이러한 점이 또 다른 debug tool로 활용되는데 도움을 줍니다.

이러한 정보에 대해, 직접 접근해 볼수도 있습니다. 예를 들어,

```
>>> import sys
>>> sys.last_traceback.tb_lineno
42
>>> sys.last_value
AssertionError('assert result == "ok"',)
```

## Dropping to PDB (Python Debugger) at the start of a test
pytest는 command line option을 통해 각각의 test 시작 시점에 PDB를 실행시킬 수 있습니다.

```
pytest --trace
```
위의 명령어가 각 테스트 실행시점에서 Python debugger를 실행시킵니다.

## Setting breakpoints
breakpoint를 코드 내에서 설정하려면, import pdb; pdb.set_trace()를 코드 내에서 불러오면 됩니다. pytest가 자동적으로 그 테스트에 대한 출력 capture를 멈출 것입니다.

다른 테스트 내에 있는 출력 capture는 영향을 받지 않습니다.
다른 이전의 이미 capture되었던 출력들은 이후, 그렇게 절차대로 처리될 것입니다.
출력 capture는 debugger 세션이 종료된 후, continue라는 command를 통해 다시 재개됩니다.
내장된 breakpoint 함수를 사용해서도 breakpoint를 설정할 수 있습니다.

Python 3.7 에서 내장된 breakpoint() 함수를 소개했습니다. 다음과 같은 방법으로 Pytest가 breakpoint() 사용을 가능케 합니다.

breakpoint() 함수가 불리고,  PYTHONBREAKPOINT가 기본값으로 설정되면, pytest는 시스템 내 있는 Pdb 대신, custom화된 내장된 PDB trace UI를 사용합니다.
테스트들이 완료되면, 시스템은 다시 시스템 PDB trace UI로 돌아갑니다.

--pdb 옵션과 함께 pytest로 넘어가면, custom internal Pdb trace UI가 breakpoint()와 실패한 테스트들 그리고 다루어지지 않은 예외상황에서도 사용됩니다.
--pdbcls는 custom debugger class를 구체화하는데 쓰일 수 있습니다.

## 테스트 실행기간 관련정보 확인하기
제일 느렸던 10개의 테스트 기간 리스트 받아내기.

pytest --durations=10
기본적으로 pytest는, -vv 옵션 flag없이는, 너무 test기간이 짧은(<0.01s)테스트들은 보여주지 않습니다.
: --vv 옵션 flag로 테스트 기간이 짧았던 test들에 대한 정보도 보여줍니다.

## Creating JUnitXML format files
Jenkins나 다른 계속되는 통합 서버에 의해 읽혀지는 결과 파일을 다음과 같은 실행방법으로 생성할 수 있습니다.

pytest --junitxml=path
지정된 경로에 XML 파일을 생성할 수 있습니다.

root test suite xml 아이템에 대한 이름을 설정하려면, junit_suite_name_option 부분을 config file에서 설정해야 합니다.

[pytest]
junit_suite_name = my_suite
New in version 4.0.

JUnix XML 스펙사항은 설치사항과 부분적인 부분을 포함해서, "time" 시간이 꼭 총 테스트 실행 시간을 보고해야 하는 것으로 보입니다. 이것은 기본적인 pytest 방식이고, 그저 call 기간만 보기 위해서는 junit_duration_report option을 다음과 같이 설정해야 합니다.

```
[pytest]
junit_duration_report = call
record_property
만약에 테스트에 관한 추가적인 정보를 기록하고 싶다면, record_property fixture를 사용하면 됩니다.

def test_function(record_property):
    record_property("example_key", 1)
    assert True
이것이 추가로 example_key="1"을 생성된 testcase tag에 붙입니다.

<testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
  <properties>
    <property name="example_key" value="1" />
  </properties>
</testcase>
대신에, 이러한 기능을 custom markers에 통합시킬 수 있습니다.

# content of conftest.py

def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))
And in your tests:

# content of test_function.py
import pytest


@pytest.mark.test_id(1501)
def test_function():
    assert True
Will result in:

<testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
  <properties>
    <property name="test_id" value="1501" />
  </properties>
</testcase>

*Warning*
이러한 특징들을 사용하는 것은 최신 JUnixXML schema를 위한 schema verifications을 깰 수도 있다는 사실에 유의하시기 바랍니다. 이것은 다른 CI servers들과 사용하는데에도 문제가 될 수 있습니다.

record_xml_attribute
추가로 xml 구성요소를 testcase 구성에 추가하려면, record_xml_attribute fixture를 사용해야 합니다. 이것은 기존에 존재하는 값들을 덮어쓰는데 사용될 수도 있습니다.


[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
