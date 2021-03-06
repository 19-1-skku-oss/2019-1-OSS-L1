---
layout: post
title: Using pytest with an existing test suite
summary: Chapter 3
featured-img: entrepreneur
---

# Using pytest with an existing test suite

Pytest can be used with most existing test suites, but its behavior differs from other test runners such as [nose]("chapter_16") or Python’s default unittest framework

Before using this section you will want to [install pytest]("https://github.com/19-1-skku-oss/2019-1-OSS-L1/blob/master/doc/kr/1.%20installation%20and%20getting%20start.md").
<br>


## Running an existing test suite with pytest

Say you want to contribute to an existing repository somewhere. After pulling the code into your development space
using some flavor of version control and (optionally) setting up a virtualenv you will want to run:
```
cd <repository>
pip install -e .    # Environment dependent alternatives include
		    # 'python setup.py develop' and 'conda develop'
```
in your project root. This will set up a symlink to your code in site-packages, allowing you to edit your code while
your tests run against it as if it were installed.
Setting up your project in development mode lets you avoid having to reinstall every time you want to run your tests,
and is less brittle than mucking about with sys.path to point your tests at local code.

Also consider using [tox]("chapter_23.4").
