---
title: "pytest fixture(3)"
date: 2019-06-08 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---


매개 변수화된 fixture에 표시하기
---
`pytest.param()`은 `@pytest.mark.parametrize`같이 매개 변수화 된 fixture 값 세트에 표시를 하는데 사용할 수 있습니다.

예를 들어:
```python
# content of test_fixture_marks.py
import pytest
@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
	return request.param

def test_data(data_set):
	pass
```
이 테스트를 실행 하면 값이 2인 `data_set` 호출을 건너 뜀니다.
```
$ pytest test_fixture_marks.py -v
========================= test session starts ==========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collecting ... collected 3 items

test_fixture_marks.py::test_data[0] PASSED [ 33%]
test_fixture_marks.py::test_data[1] PASSED [ 66%]
test_fixture_marks.py::test_data[2] SKIPPED [100%]
================= 2 passed, 1 skipped in 0.12 seconds ==================
```


모듈화: fixture 함수에서 fixture 사용하기
---
테스트 함수에서 fixture를 사용할 수 는 없지만 fixture 함수는 다른 fixture를 직접 사용할 수 있습니다. 이것은 fixture의 모듈 디자인에 기여하고 많은 프로젝트에서 framework별로 fixture를 재사요 할 수 있게 합니다. 간단한 예로서 이전 예제를 확장하는 이미 정의 된 `smtp_connection` 리소스를 여기에 붙여 넣은 `app` 객체를 인스턴스화 할 수 있습니다.
```python
# content of test_appsetup.py

import pytest

class App(object):
	def __init__(self, smtp_connection):
		self.smtp_connection = smtp_connection

@pytest.fixture(scope="module")
def app(smtp_connection):
	return App(smtp_connection)

def test_smtp_connection_exists(app):
	assert app.smtp_connection
```
여기서는 이전의 정의 된 `smtp_connection` fixture를 받아 와서 `App` 객체를 인스턴스화 하는 `app` fixture를 선언합니다. 이것을 실행하면 다음과 같습니다.
```
$ pytest -v test_appsetup.py
========================= test session starts ==========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collecting ... collected 2 items

test_appsetup.py::test_smtp_connection_exists[smtp.gmail.com] PASSED [ 50%]
test_appsetup.py::test_smtp_connection_exists[mail.python.org] PASSED [100%]

======================= 2 passed in 0.12 seconds =======================
```
`smtp_connection`의 매개 변수화로 인해 이 테스트는 두개의 서로 다른 `App` 인스턴스와 각각의 smtp 서버로 두번 실행됩니다. pytest가 fixture의 의존성 그래프를 완전히 분석하기 때문에 `app` fixture가 `smtp_connection` 매개 변수를 인식 할 필요가 없습니다.
`app` fixture는 모듈 범위를 갖고 있으며 모듈 범위의 `smtp_connection` fixture를 사용합니다. 이 예제는 `smtp_conneciton`이 session 범위에 캐시 된 경우에도 계속 작동합니다. fixture가 더 넓은 범위의 fixture를 사용하는 것은 가능하지만 session 범위에서 모듈 범위의 fixture를 사용하는 것 처럼 반대로는 사용할 수 없습니다.

Fixture 인스턴스에 의한 테스트의 자동 그룹화
---

pytest는 테스트 실행 중에 활성화된 fixture의 수를 최소화합니다. 매개 변수화 된 fixture가 있다면, 그것을 사용하는 모든 테스트는 먼저 하나의 인스턴스로 실행되고 다음 fixture 인스턴스가 생성되기 전에 finalizer가 호출됩니다. 무엇보다도 global state를 만들고 사용하는 응용 프로그램 테스트가 쉬워집니다.
다음 예제는 두 개의 매개 변수화 된 fixture를 사용하며 그 중 하나는 모듈 단위로 범위가 지정되며 모든 함수는 `print` 호출을 수행하여 setup/teardown 흐름을 표시합니다.
```python
# content of test_module.py
import pytest

@pytest.fixture(scope="module", params=["mod1", "mod2"])
def modarg(request):
	param = request.param
	print(" SETUP modarg %s" % param)
	yield param
	print(" TEARDOWN modarg %s" % param)

@pytest.fixture(scope="function", params=[1,2])
def otherarg(request):
	param = request.param
	print(" SETUP otherarg %s" % param)
	yield param
	print(" TEARDOWN otherarg %s" % param)

def test_0(otherarg):
	print(" RUN test0 with otherarg %s" % otherarg)
def test_1(modarg):
	print(" RUN test1 with modarg %s" % modarg)
def test_2(otherarg, modarg):
	print(" RUN test2 with otherarg %s and modarg %s" % (otherarg, modarg))
```
테스트를 상세 모드(verbose)로 실행하고 `print` 출력을 살펴 봅시다.
```
$ pytest -v -s test_module.py
========================= test session starts ==========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collecting ... collected 8 items

test_module.py::test_0[1] SETUP otherarg 1
	RUN test0 with otherarg 1
PASSED TEARDOWN otherarg 1

test_module.py::test_0[2] SETUP otherarg 2
	RUN test0 with otherarg 2
PASSED TEARDOWN otherarg 2

test_module.py::test_1[mod1] SETUP modarg mod1
	RUN test1 with modarg mod1
PASSED
test_module.py::test_2[mod1-1] SETUP otherarg 1
	RUN test2 with otherarg 1 and modarg mod1
PASSED TEARDOWN otherarg 1

test_module.py::test_2[mod1-2] SETUP otherarg 2
	RUN test2 with otherarg 2 and modarg mod1
PASSED TEARDOWN otherarg 2

test_module.py::test_1[mod2] TEARDOWN modarg mod1
SETUP modarg mod2
	RUN test1 with modarg mod2
PASSED
test_module.py::test_2[mod2-1] SETUP otherarg 1
	RUN test2 with otherarg 1 and modarg mod2
PASSED TEARDOWN otherarg 1

test_module.py::test_2[mod2-2] SETUP otherarg 2
	RUN test2 with otherarg 2 and modarg mod2
PASSED TEARDOWN otherarg 2
TEARDOWN modarg mod2

========================= 8 passed in 0.12 seconds =========================
```
매개 변수화 된 모듈 범위의 `modarg` 리소스가 가능한 가장 적은 활성화 된 리소스로 이어지는 테스트 실행 순서를 발생 시켰음을 알 수 있습니다. `mod1`의 매개 변수화 된 리소스의 finalizer는 `mod1`의 리소스가 설정 되기 전에 실행되었습니다.
특히 `test_0`은 완전히 독립적이며 처음에 끝납니다. 그런 다음 `test_1`을 `mod1`로 실행 한 다음 `test_2`를 `mod1`로 실행 한 다음 `test_1`을 `mod2`로 실행하고 마지막으로 `test_2`를 `mod2`로 실행합니다.
다른 매개 변수화 된 자원(함수 범위를 가진)은 그것을 사용했던 모든 테스트가 끝나기 전에 설정되고 해제되었습니다.

클래스, 모듈 또는 프로젝트에서 fixture 사용
---
때때로 테스트 함수는 fixture 객체에 직접 접근할 필요가 없습니다. 예를 들어 테스트는 빈 디렉토리를 현재 작업 디렉토리로 사용해야 하지만 그렇지 않으면 구체적인 디렉토리를 고려하지 않을 수도 있습니다. 다음은 표준 `tempfile` 및 pytest fixture를 사용하는 방법입니다. 우리는 fixture의 생성을 `conftest.py`파일로 분리합니다.
```python
# content of conftest.py

import pytest
import tempfile
import os

@pytest.fixture()
def cleandir():
	newpath = tempfile.mkdtemp()
	os.chdir(newpath)
```
`usefixtures` 표시를 통해 테스트 모듈에서 그 사용을 선언합니다.
```python
# content of test_setenv.py
import os
import pytest

@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit(object):
	def test_cwd_starts_empty(self):
		assert os.listdir(os.getcwd()) == []
		with open("myfile", "w") as f:
			f.write("hello")

	def test_cwd_again_starts_empty(self):
		assert os.listdir(os.getcwd()) == []
```
`usefixtures`마커로 인해 각 테스트 메소드 실행시 `cleandir` fixture가 필요할 것 입니다. 마치 각 메소드에 `cleandir` 함수 인수를 지정한 것과 같습니다. 우리의 fixture가 작동하고 테스트가 통과되는지 확인하기 위헤 실행시켜 보았습니다.
```
$ pytest -q
.. 									[100%]
2 passed in 0.12 seconds
```
다음과 같이 여러 fixture를 지정할 수 있습니다.
```python
@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
	...
```
mark 메커니즘의 일반적인 기능을 사 용하여 테스트 모듈 수준에서 fixture 사용을 지정할 수 있습니다.
```
pytestmark = pytest.mark.usefixtures("cleandir")
```
할당 된 변수는 `pytestmark`로 호출되어야 합니다. `foomark`는 fixture를 활성화 하지 않습니다.
또한 프로젝트의 모든 테스트에 필요한 fixture를 ini-file에 넣는 것도 가능합니다.
```python
# content of pytest.ini
[pytest]
usefixtures = cleandir
```