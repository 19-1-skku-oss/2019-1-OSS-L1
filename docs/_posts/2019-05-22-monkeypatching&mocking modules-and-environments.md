---
layout: post
title: "Monkeypatching/mocking modules and environments"
summary: Chapter 7
featured-img: startup
---

종종 테스트를 진행할 때 글로벌 세팅이나 네트워크 접근과 같은 상황에서 코드를 불러 와야하는 어려운 상황이 있습니다.<br>
Pytest에서 제공하는 The monkeypatch fixture 는 이를 불러 오는데에 큰 역할을 합니다.


## 7.1 monkeypatching functions의 간단한 예제
os.expanduser가 특정 주소를 반환하게 하려면, the monkeypatch를 사용하면 됩니다.
os.expanduser 호출하기 전에 setattr() 를 사용해야합니다.
예시:

```python
# content of test_module.py
import os.path
def getssh(): # pseudo application code
    return os.path.join(os.path.expanduser("~admin"), '.ssh')

def test_mytest(monkeypatch):
    def mockreturn(path):
        return '/abc'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    x = getssh()
    assert x == '/abc/.ssh'
```



## 7.2 Global patch example: preventing “requests” from remote operations
requests라이브러리가 당신의 테스트 코드에서 http requests를 시행하는 것을 방지하기 위해서는 이렇게 하세요:
```python
# content of conftest.py
import pytest
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")
```


## 7.3 Monkeypatching 환경 변수
환경 변수를 가지고 작업을 한다면, 당신은 시스템에서 테스팅을 위해 안전하게 값을 변경하거나 지워야 할 것입니다. Monkeypatch는 이를 위해 setenv and delenv를 사용하여 이를 지원합니다:

```python
# contents of our original code file e.g. code.py
import os

def get_os_user_lower():
        """Simple retrieval function.
        Returns lowercase USER or raises EnvironmentError."""
        username = os.getenv("USER")
       
        if username is None:
            raise EnvironmentError("USER environment is not set.")
        
        return username.lower()
```


두 가지 상황이 존재 할 수 있는데, 첫번째는 유저 환경 변수를 하나의 값으로 세팅 되어 있는 것입니다. 두번째는 유저 환경 변수가 존재하지 않는 상황입니다. monkeypatch는 실행 환경에 영향을 주지 않고 안전하게 두 상황에서 모두 테스팅 가능하게 합니다:
```python
# contents of our test file e.g. test_code.py
import pytest

def test_upper_to_lower(monkeypatch):
        """Set the USER env var to assert the behavior."""
        monkeypatch.setenv("USER", "TestingUser")
        assert get_os_user_lower() == "testinguser"
def test_raise_exception(monkeypatch):
"""Remove the USER env var and assert EnvironmentError is raised."""
monkeypatch.delenv("USER", raising=False)
with pytest.raises(EnvironmentError):
_ = get_os_user_lower()
```


This behavior can be moved into fixture structures and shared across tests:
```python
import pytest

@pytest.fixture
def mock_env_user(monkeypatch):
    monkeypatch.setenv("USER", "TestingUser")
    
@pytest.fixture
def mock_env_missing(monkeypatch):
    monkeypatch.delenv("USER", raising=False)
    
# Notice the tests reference the fixtures for mocks
def test_upper_to_lower(mock_env_user):
    assert get_os_user_lower() == "testinguser"
    
def test_raise_exception(mock_env_missing):
    with pytest.raises(EnvironmentError):
         _ = get_os_user_lower()
```

