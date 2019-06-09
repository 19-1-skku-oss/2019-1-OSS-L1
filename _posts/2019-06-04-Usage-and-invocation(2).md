---
title: "사용법 그리고 실행방법(2)"
date: 2019-06-04 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---
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
```
