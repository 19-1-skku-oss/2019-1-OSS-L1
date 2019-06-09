---
layout: post
title: "Temporary directories and files"
summary: Chapter 8
featured-img: code2
---


## 8.1 The tmp_path fixture
You can use the tmp_path fixture which will provide a temporary directory unique to the test invocation, created in
the base temporary directory.
tmp_path is a pathlib/pathlib2.Path object. Here is an example test usage:

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

Running this would result in a passed test except for the last assert 0 line which we use to look at values:
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
The tmp_path_factory is a session-scoped fixture which can be used to create arbitrary temporary directories
from any other fixture or test.
It is intended to replace tmpdir_factory, and returns pathlib.Path instances.

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
You can use the tmpdir fixture which will provide a temporary directory unique to the test invocation, created in the
base temporary directory.
tmpdir is a py.path.local object which offers os.path methods and more. Here is an example test usage:

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

Running this would result in a passed test except for the last assert 0 line which we use to look at values:
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
Temporary directories are by default created as sub-directories of the system temporary directory. The base name
will be pytest-NUM where NUM will be incremented with each test run. Moreover, entries older than 3 temporary
directories will be removed.
You can override the default temporary directory setting like this:

```python
pytest --basetemp=mydir
```
