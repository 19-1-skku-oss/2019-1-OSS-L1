Sometimes tests need to invoke functionality which depends on global settings or which invokes code which cannot be
easily tested such as network access. The monkeypatch fixture helps you to safely set/delete an attribute, dictionary
item or environment variable or to modify sys.path for importing. See the monkeypatch blog post for some
introduction material and a discussion of its motivation.

## 7.1 Simple example: monkeypatching functions
If you want to pretend that os.expanduser returns a certain directory, you can use the monkeypatch.
setattr() method to patch this function before calling into a function which uses it:

'''

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
'''

Here our test function monkeypatches os.path.expanduser and then calls into a function that calls it. After the
test function finishes the os.path.expanduser modification will be undone.

## 7.2 Global patch example: preventing “requests” from remote operations
If you want to prevent the “requests” library from performing http requests in all your tests, you can do:
# content of conftest.py
import pytest
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
monkeypatch.delattr("requests.sessions.Session.request")

## 7.3 Monkeypatching environment variables
If you are working with environment variables you often need to safely change the values or delete them from the
system for testing purposes. Monkeypatch provides a mechanism to do this using the setenv and delenv
method. Our example code to test:

'''
# contents of our original code file e.g. code.py
import os
def get_os_user_lower():
        """Simple retrieval function.
        Returns lowercase USER or raises EnvironmentError."""
        username = os.getenv("USER")
       
        if username is None:
        raise EnvironmentError("USER environment is not set.")
        
        return username.lower()
'''

There are two potential paths. First, the USER environment variable is set to a value. Second, the USER environment
variable does not exist. Using monkeypatch both paths can be safely tested without impacting the running
environment:
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


## 7.4 API Reference
Consult the docs for the MonkeyPatch class.
