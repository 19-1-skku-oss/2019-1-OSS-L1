---
title: "Doctest integration for modules and test files"
date: 2019-06-09 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---


기본적으로 test*.txt에 매칭되는 파일은 파이썬 스탠다드 모듈에서 실행됩니다. 이 패턴은 다음 코드를 실행함으로 바꿀 수 있습니다.

```
pytest --doctest-glob='*.rst'
```

--doctest-glob는 커맨드 라인에서 여러 번 주어질 수 있습니다.
다음과 같은 텍스트 파일이 있다면 당신은 pytest를 바로 실행시킬 수 있습니다.

```
# content of test_example.txt
hello this is a doctest
>>> x = 3
>>> x
3
```

실행 예시:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item
test_example.txt . [100%]
========================= 1 passed in 0.12 seconds =========================
```

pytest는 기본적으로 doctest directives를 찾기위해 test*.txt가 허용 된 상태입니다.


```python
# content of mymodule.py
def something():
""" a doctest in a docstring
>>> something()
42
"""
return 42
```

```
$ pytest --doctest-modules
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 2 items
mymodule.py . [ 50%]
test_example.txt . [100%]
========================= 2 passed in 0.12 seconds =========================
```

## 11.1 Encoding
디폴트 인코딩은 UTF-8이지만 doctest_encoding ini옵션을 사용하는 doctest파일에 사용되는 인코딩을 구체화 할 수 있습니다:

```
# content of pytest.ini
[pytest]
doctest_encoding = latin1
```


## 11.2 Using ‘doctest’ options
일반적인 doctest module는 doctest tests의 엄격성을 제공하기 위해 몇가지의 옵션을 제공합니다. <
Pytest에서는 configuration file을 사용함으로써 앞선 기능들을 사용할 수 있습니다.

```
[pytest]
doctest_optionflags= NORMALIZE_WHITESPACE IGNORE_EXCEPTION_DETAIL
```


```
# content of example.rst
>>> get_unicode_greeting() # doctest: +ALLOW_UNICODE
'Hello'
```

기본적인 설정에 의해, Pytest는 주어진 doctest에 대해 가장 처음 failure만 알려줄 것 입니다. 만약 당신이 failure가 있어도 테스트를 진행하고 싶다면:
```
pytest --doctest-modules --doctest-continue-on-failure
```


## 11.3 Output format
다음 옵션들을 사용하여 failure에 대한 출력 포맷을 바꿀 수 있습니다.

```
pytest --doctest-modules --doctest-report none
pytest --doctest-modules --doctest-report udiff
pytest --doctest-modules --doctest-report cdiff
pytest --doctest-modules --doctest-report ndiff
pytest --doctest-modules --doctest-report only_first_failure
```



## 11.4 pytest-specific features
Pytest에서는 doctests를 만드는 과정을 더 쉽게하거나 당신이 이미 가진 test suite와의 더 나은 통합을 위해 제공하는 기능들이 있습니다.<br>
이러한 기능들을 잘 사용하면 일반적인 doctests module를 사용하는 것에 비해 훨씬 효율적입니다.



### 11.4.1 Using fixtures
'getfixture helper'를 사용하여 fixture 사용이 가능합니다:

```
# content of example.rst
>>> tmp = getfixture('tmpdir')
>>> ...
>>>
```


### 11.4.2 ‘doctest_namespace’ fixture
doctest_namespace fixture는 당신의 doctests가 실행되고 있는 namespace에 아이템을 넣는데에 사용될 수 있습니다.<br>
doctest_namespace는 일반적인 dict 오브젝트이며 그곳에는 당신이 doctest에서 나타나기를 원하는 오브젝트를 위치시킬 수 있습니다.

```python
# content of conftest.py
import numpy
@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace['np'] = numpy
```

다음과 같이 doctests 바로 사용될 수 있습니다:

```python
# content of numpy.py
def arange():
    """
    >>> a = np.arange(10)
    >>> len(a)
    10
    """
    pass
```



## 11.4.3 Skipping tests dynamically
pytest.skip 명령어를 사용하여 동적으로 doctest를 넘어갈 수 있습니다. 예를 들어: 

```python
>>> import sys, pytest
>>> if sys.platform.startswith('win'):
... pytest.skip('this doctest does not work on Windows')
...
```
