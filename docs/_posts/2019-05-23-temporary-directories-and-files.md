---
layout: post
title: "Temporary directories and files"
summary: Chapter 8
featured-img: code2
---


## 8.1 The tmp_path fixture
tmp_path fixture 를 사용해서 테스트를 부르는데 임시 주소를 제공합니다.
tmp_path는 pathlib/pathlib2.Path object입니다. 예시: 

```python
# content of test_tmp_path.py
import os

CONTENT = u"content"

def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0
```

위 코드를 pytest로 테스트한 결과:
```
$ pytest test_tmp_path.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item

test_tmp_path.py F [100%]

================================= FAILURES =================================
_____________________________ test_create_file _____________________________
tmp_path = PosixPath('PYTEST_TMPDIR/test_create_file0')
      def test_create_file(tmp_path):
      d = tmp_path / "sub"
      d.mkdir()
      p = d / "hello.txt"
      p.write_text(CONTENT)
      assert p.read_text() == CONTENT
      assert len(list(tmp_path.iterdir())) == 1
>     assert 0
E     assert 0
test_tmp_path.py:13: AssertionError
========================= 1 failed in 0.12 seconds =========================
```

## 8.2 The tmp_path_factory fixture
tmp_path_factory는 다른 테스트나 fixture로 부터 임의적인 임시 주소를 만드는데 사용되는 fixture입니다.
이것은 tmpdir_factory를 다른 곳에 위치 시키고,  pathlib.Path instances 반환하게 하기 위함입니다.

```python
# contents of conftest.py

import pytest
@pytest.fixture(scope="session")
  def image_file(tmpdir_factory):
      img = compute_expensive_image()
      fn = tmpdir_factory.mktemp("data").join("img.png")
      img.save(str(fn))
      return fn
# contents of test_image.py
def test_histogram(image_file):
    img = load_image(image_file)
    # compute and test histogram

```


## 8.3 The ‘tmpdir’ fixture
the tmpdir fixture는 테스트를 부를 때마다 고유의 임시 주소를 제공하고 기본 임시 주소에 만들어지는 fixture입니다.
tmpdir 는 os.path methods와 기타 다른 기능을 제공하는 py.path.local 오브젝트입니다
예시:

```python
# content of test_tmpdir.py
import os
def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    assert 0
```

위 코드를 pytest로 실행한 결과:
```
$ pytest test_tmpdir.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item
test_tmpdir.py F [100%]

================================= FAILURES =================================
_____________________________ test_create_file _____________________________
tmpdir = local('PYTEST_TMPDIR/test_create_file0')

    def test_create_file(tmpdir):
        p = tmpdir.mkdir("sub").join("hello.txt")
        p.write("content")
        assert p.read() == "content"
        assert len(tmpdir.listdir()) == 1
>       assert 0
E       assert 0

test_tmpdir.py:7: AssertionError
========================= 1 failed in 0.12 seconds =========================
```


## 8.4 The default base temporary directory
임시 주소는 기본적으로 시스템 임시 주소 안에 서브 다이렉토리로 만들어집니다. 기본 이름은 pytest-NUM이고 'NUM'의 경우 하나의 테스트를 실행할 때마다 증가됩니다.
세 개 임시주소 이상을 가지고 있다면 주소가 모두 지워집니다. 
기본 임시 주소를 오버라이드 해서 사용할 수 있습니다:

```python
pytest --basetemp=mydir
```
