---
layout: post
title: "Usage and Invocations(1)"
summary: Chapter 2
featured-img: sleek
---

# 사용법 그리고 실행방법

Terminal command로 python을 이용하더라도, -m 옵션 flag를 통해 pytest를 실행할 수 있습니다.
: python -m pytest

python -m pytest가 현재 위치의 directory를 sys.path에 저장한다는 사실 이외에는 사실상 pytest 명령어와 다를 것이 없습니다.
<br>
<br>


## 가능한 종료 상황(exit codes)들은 총 6가지 경우가 있습니다.

모든 테스트들이 성공적으로 모여지고 통과된 경우, Exit code 0

테스트들이 모여지고, 실행되어졌지만 부분적으로 실패한 경우, Exit code 1

유저에 의해 Test가 중지된 경우, Exit code 2

테스트 실행 중 내부 에러가 발생한 경우, Exit code 3

Terminal 상의 pytest command line 사용법에 error가 생긴 경우, Exit code 4

단 하나의 테스트도 모이지 않은 경우, Exit code 5
<br>
<br>



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
<br>
<br>



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
<br>
<br>
<br>



[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
