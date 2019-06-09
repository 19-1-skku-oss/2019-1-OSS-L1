---
layout: post
title: "Usage and Invocations(1)"
summary: Chapter 2
featured-img: sleek
---

# Usage and Invocations

## Calling pytest through python -m pytest

You can invoke testing through the Python interpreter from the command line:
```
python -m pytest [...]
```

This is almost equivalent to invoking the command line script pytest [...] directly, except that calling via
python will also add the current directory to sys.path.
<br>
<br>


## Possible exit codes

Running pytest can result in six different exit codes:
- Exit code 0 All tests were collected and passed successfully
- Exit code 1 Tests were collected and run but some of the tests failed
- Exit code 2 Test execution was interrupted by the user
- Exit code 3 Internal error happened while executing tests
- Exit code 4 pytest command line usage error
- Exit code 5 No tests were collected


## Getting help on version, option names, environment variables

```
pytest --version   # shows where pytest was imported from
pytest --fixtures  # show available builtin function arguments
pytest -h | --help # show help on command line and config file options
```

To stop the testing process after the first (N) failures:

```
pytest -x            # stop after first failure
pytest --maxfail=2    # stop after two failures
```
## Specifying tests / selecting tests
Pytest supports several ways to run and select tests from the command-line.


#### Run tests in a module

```
pytest test_mod.py
```
#### Run tests in a directory

```
pytest testing/
```

#### Run tests by keyword expressions

```
pytest -k "MyClass and not method"
```
This will run tests which contain names that match the given string expression, which can include Python operators
that use filenames, class names and function names as variables<br>

#### Run tests by node ids

Each collected test is assigned a unique nodeid which consist of the module filename followed by specifiers like
class names, function names and parameters from parametrization, separated by :: characters.

To run a specific test within a module:

```
pytest test_mod.py::test_func
```
Another example specifying a test method in the command line:

```
pytest test_mod.py::TestClass::test_method
```
#### Run tests by marker expressions

```
pytest -m slow
```
Will run all tests which are decorated with the @pytest.mark.slow decorator
<br>
<br>
<br>



[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
