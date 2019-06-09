---
title: "The writing and reporting of assertions in tests"
date: 2019-06-03 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---

## 4.1 Asserting with the assert statement

기존 Python의 'assert' 명령어를 Pytest에서도 사용 가능합니다.
다음 예제 코드에서 assert명령을 사용함으로써 함수가 특정값을 리턴한다는 것을 확인합니다.

<pre><code>
# content of test_assert1.py
def f():
   return 3
def test_function():
   assert f() == 4
</code></pre>

함수 f()가 assert한 값과 다른 값을 리턴할 때 fail 되는 예시코드:
<pre><code>
$ pytest test_assert1.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item
test_assert1.py F                                                     [100%]
================================= FAILURES =================================
______________________________ test_function _______________________________
     def test_function():
>       assert f() == 4
E       assert 3 == 4
E           + where 3 = f()
test_assert1.py:6: AssertionError
========================= 1 failed in 0.12 seconds =========================
</code></pre>

또한 pytest의 assert 함수호출, 비교, 이진수 등 가장 일반적인(대표적인) 표기들을 모두 지원합니다. 



## 4.2 Assertions about expected exceptions
예상되는 예외(exception)에 대한 assert를 작성하고자 할 때에는 pytest.raises를 사용합니다:
<pre><code>
import pytest
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
         1 / 0
</code></pre>

예외에 대한 정보를 직접적으로 얻고 싶을 경우에는 다음 코드를 참고하세요:
<pre><code>
def test_recursion_depth():
     with pytest.raises(RuntimeError) as excinfo:
     <br>
      def f():
          f()
          <br>
        f()
     assert "maximum recursion" in str(excinfo.value)
</code></pre>

'Match' 키워드를 사용함으로써 스트링으로 나타낸 예외 상황과 넘겨 받은 파라미터가 매치하는지 확인할 수 있습니다.
<pre><code>
import pytest
def myfunc():
   raise ValueError("Exception 123 raised")
def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
</code></pre>



## 4.3 Assertions about expected warnings
pytest.warns. 명령어를 사용하면 해당 코드가 특정 경고를 발생시키는지 확인할 수 있습니다.


## 4.4 Making use of context-sensitive comparisons
pytest는 또한 비교(comparision) 상황을 맞닥뜨렸을때 다양한 정보를 알려줍니다. 예를 들어:
<pre><code>
# content of test_assert2.py
<br>
def test_set_comparison():
   set1 = set("1308")
   set2 = set("8035")
   assert set1 == set2
</code></pre>

위 코드를 pytest로 검사하면:
<pre><code>
$ pytest test_assert2.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item
test_assert2.py F [100%]
================================= FAILURES =================================
___________________________ test_set_comparison ____________________________
      def test_set_comparison():
            set1 = set("1308")
            set2 = set("8035")
>           assert set1 == set2
E           AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
E           Extra items in the left set:
E           '1'
E           Extra items in the right set:
E           '5'
E            Use -v to get the full diff
test_assert2.py:6: AssertionError
========================= 1 failed in 0.12 seconds =========================
</code></pre>

이렇게 비교과정을 pytest를 통해 자세히 알 수 있습니다.


## 4.5 Defining your own explanation for failed assertions
'pytest_assertrepr_compare hook' 명령어를 사용하면 실패한 assertion에 대해 자신만의 각주/설명을 달 수 있습니다.

pytest_assertrepr_compare(config, op, left, right)
<br>
      Parameters config (_pytest.config.Config) – pytest config object
 
FOO 오브젝트에 대한 다른 설명을 제공하는 파일:
<pre><code>
# content of conftest.py
from test_foocompare import Foo


def pytest_assertrepr_compare(op, left, right):
   if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
      return ["Comparing Foo instances:", " vals: %s != %s" % (left.val, right.˓→val)]
</code></pre>

<pre><code>
# content of test_foocompare.py
class Foo(object):
      def __init__(self, val):
         self.val = val
         
      def __eq__(self, other):
         return self.val == other.val
         
def test_compare():
      f1 = Foo(1)
      f2 = Foo(2)
      assert f1 == f2
</code></pre>

위 코드를 pytest를 통해 검토한 결과:
<pre><code>
$ pytest -q test_foocompare.py
F [100%]
================================= FAILURES =================================
_______________________________ test_compare _______________________________
   def test_compare():
         f1 = Foo(1)
         f2 = Foo(2)
>        assert f1 == f2
E        assert Comparing Foo instances:
E              vals: 1 != 2
test_foocompare.py:12: AssertionError
1 failed in 0.12 seconds
</code></pre>

## 4.6 Assertion introspection details
Assertion이 실패하면 제공되는 디테일한 정보들은 assertion이 실행되기 전에 해당 선언을 다시 작성해 놓는 방식으로 가능해집니다.


### 4.6.1 Assertion rewriting caches files on disk
Pytest는 캐싱을 위해 디스크에 모듈을 다시 작성합니다. 이 작업을 막기 위해서는 다음 명령어를 코드 가장 위쪽에 작성해야합니다:

<pre><code>
import sys
sys.dont_write_bytecode = True
</code></pre>

Assert명령을 사용하는 것에는 다름이 없지만 해당 코드파일이 디스크에 캐싱이 되지 않는다는 차이가 존재합니다.


### 4.6.2 Disabling assert rewritin
assert가 다시 써지는 것을 방지하기 위해서 다양한 옵션이 존재합니다.

• Disable rewriting for a specific module by adding the string PYTEST_DONT_REWRITE to its docstring.
• Disable rewriting for all modules by using --assert=plain.
Add assert rewriting as an alternate introspection technique.
Introduce the --assert option. Deprecate --no-assert and --nomagic.
Removes the --no-assert and --nomagic options. Removes the --assert=reinterp
option.
