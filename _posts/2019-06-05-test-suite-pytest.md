---
title: "기존 시험장에서의 pytest"
date: 2019-06-05 08:26:28 -0400
categories:
  - pytest document
sidebar:
  nav: "docs"
---
<br>


# 기존의 시험장(test suite)에서의 pytest

pytest는 대부분의 기존 시험장을 사용할 수 있습니다. 하지만 pytest는 [nose]("chapter_16")나 다른 Python의 기본적인 unittest framework와는 다르게 작동합니다.

이후의 내용을 위해 먼저 [pytest를 설치]("https://github.com/19-1-skku-oss/2019-1-OSS-L1/blob/master/doc/kr/1.%20installation%20and%20getting%20start.md")해주세요.
<br>

3.1 기존의 시험장에서의 pytest
---
기존의 저장소에 기여하고 싶다면, 버전 제어의 일부 기능을 사용하여 코드를 당신의 개발 공간으로 pulling 해온 후에, 원한다면 당신이 실행할 가상환경을 당신의 project root에 설치하세요.
```
cd <repository>
pip install -e .    # Environment dependent alternatives include
		    # 'python setup.py develop' and 'conda develop'
```
이는 site packages 안의 당신의 코드에 심볼릭 링크를 생성해주며, 당신의 테스트가 설치되어 있는 것 처럼 실행하며 수정할 수 있습니다.
당신의 프로젝트를 개발모드로 설치하면 당신의 코드를 테스트할 때마다 당신의 코드를 재설치 하지 않아도 됩니다. 또한, 당신의 테스트를 local code로  가리키기 위해 sys.path를 건들이는 것 보다 덜 위험합니다.

또한 [tox]("chapter_23.4")를 사용하는 것을 고려해보세요.
