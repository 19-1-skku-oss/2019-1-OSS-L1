---
layout: post
title: "pytest fixture(2)"
summary: Chapter 5-2
featured-img: code
---

Fixture 종료/ teardown 코드 실행
---
pytest는 fixtrue의 범위를 벗어 났을 때 특정 fixtuer의 종료 코드 실행을 지원합니다. `return` 대신 `yield`문을 사용하면 `yield`문 다음의 모든 코드가 teardown 코드로 사용됩니다.
```python
# content of conftest.py

import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection():
	smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
	yield smtp_connection # provide the fixture value
	print("teardown smtp")
	smtp_connection.close()
```
테스트의 예외 상황과는 상관 없이, `print`와 `stmp.close()` 구문은 모듈 내의 마지막 테스트가 끝난 후에 실행됩니다.

이것을 실행시키면:
```
$ pytest -s -q --tb=no
FFteardown smtp

2 failed in 0.12 seconds
```
`smtp_connection` 인스턴스가 두개의 테스트 실행이 끝난 후에 종료되었음을 알 수 있습니다. 우리가 fixture 함수에 `scope='function'`이라는 옵션을 준다면, fixture setup과 teardown은 각 단일 테스트 앞뒤에서 일어납니다. 두 경우 모두 테스트 모듈 자체가 fixture 설정의 세부사항을 변경하거나 알 필요가 없습니다.

`with`문을 사용하여 `yield` 문법을 매끄럽게 사용할 수 있습니다.
```python
# content of test_yield2.py

import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection():
	with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as smtp_connection:
		yield smtp_connection # provide the fixture value
```
`with`문이 끝나면 `smtp_connection`객체가 자동으로 닫히기 때문에 테스트가 끝난 후 `smtp_connection` 연결이 닫힙니다.
setup 코드(`yield` 키워드 이전)에서 예외가 발생하면 teardown 코드(`yield`)가 호출되지 않습니다.
teardown 코드를 실행하기 위한 또 다른 옵션은 request-context 객체의 `addfinalizer` 메소드를 사용하여 종료 함수를 등록하는 것입니다.

다음은 종료를 위해 `addfinalizer`를 사용하도록 `smtp_connection` fixture를 변경 한 것입니다.
```python
# content of conftest.py
import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection(request):
	smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    
	def fin():
		print("teardown smtp_connection")
		smtp_connection.close()
        
	request.addfinalizer(fin)
	return smtp_connection # provide the fixture value
```
`yield` 및 `addfinalizer` 메서드는 테스트가 끝난 후 코드를 호출하여 비슷하게 작동하지만 `addfinalizer`에는 `yield`와 비교하여 두 가지 중요한 차이가 잇습니다.
1. 여러 finalizer 함수를 등록 할 수 있습니다.
2. fixture setup 코드가 예외를 발생 시키더라도 finalizer를 항상 호출합니다. 이것들 중 하나가 생성/획득되지 않더라도 fixture에 의해 생성된 모든 자원을 적절하게 닫는 것이 편리합니다.
```python
@pytest.fixture
def equipments(request):
	r = []
	for port in ('C1', 'C3', 'C28'):
		equip = connect(port)
		request.addfinalizer(equip.disconnect)
		r.append(equip)
	return r
```
위의 예에서 `"C28"`이 예외로 실패하더라도 `"C1"`,`"C3"`은 올바르게 닫힙니다. 물론 finalize 함수가 등록되기 전에 예외가 발생하면 실행되지 않습니다.

fixture는 요청한 테스트의 내용을 검사할 수 있습니다.
---
Fixture 함수는 요청한 객체를 받아 들여 요청하는 테스트 함수, class, 또는 모듈의 내용을 검사할 수 있습니다. 이전의 `smtp_connection` fixture 예제를 확장 한 다음, 우리의 조명기를 사용하는 테스트 모듈에서 선택적인 서버 URL을 읽습니다.
```python
# content of conftest.py
import pytest
import smtplib

@pytest.fixture(scope="module")
def smtp_connection(request):
	server = getattr(request.module, "smtpserver", "smtp.gmail.com")
	smtp_connection = smtplib.SMTP(server, 587, timeout=5)
	yield smtp_connection
	print("finalizing %s (%s)" % (smtp_connection, server))
	smtp_connection.close()
```
`Test.modlue`속성을 사용하여 선택적으로 테스트 모듈에서 `smtpserver`속성을 얻습니다. 다시 실행하면, 그다지 변한 것은 없습니다.
```
$ pytest -s -q --tb=no
FFfinalizing <smtplib.SMTP object at 0xdeadbeef> (smtp.gmail.com)

2 failed in 0.12 seconds
```
실제로 모듈 namespace에서 서버 URL을 설정하는 다른 테스트 모듈을 빠르게 만들어 보겠습니다.
```python
# content of test_anothersmtp.py

smtpserver = "mail.python.org" # will be read by smtp fixture

def test_showhelo(smtp_connection):
	assert 0, smtp_connection.helo()
```
위의 코드를 실행하면
```
$ pytest -qq --tb=short test_anothersmtp.py
F 								[100%]
=============================== FAILURES ===============================
____________________________ test_showhelo _____________________________
test_anothersmtp.py:5: in test_showhelo
	assert 0, smtp_connection.helo()
E 	AssertionError: (250, b'mail.python.org')
E 	assert 0
----------------------- Captured stdout teardown -----------------------
finalizing <smtplib.SMTP object at 0xdeadbeef> (mail.python.org)
```
`smtp_connection` fixture 함수는 모듈 namespace에서 메일 서버 이름을 가져왔습니다.

많은 fixture의 생성(Factories as fixture)
---
"factory as fixture" 패턴은 단일 테스트에서 fixture의 결과가 여러 번 필요한 상황에서 도움이 될 수 있습니다. 대신 직접 데이터를 반환하는 대신 fixture는 데이터를 생성하는 함수를 반환하비낟. 이 함수는 테스트에서 여러 번 호출 될 수 있습니다.

Factories 는 필요에 따라 매개 변수를 가질 수 있습니다.
```python
@pytest.fixture
def make_customer_record():

	def _make_customer_record(name):
		return {
			"name": name,
			"orders": []
		}

	return _make_customer_record

def test_customer_records(make_customer_record):
	customer_1 = make_customer_record("Lisa")
	customer_2 = make_customer_record("Mike")
	customer_3 = make_customer_record("Meredith")
```
factory에서 생성된 데이터의 관리가 필요하다면, fixture는 다음과 같이 처리할 수 있습니다.
```python
@pytest.fixture
def make_customer_record():

	created_records = []

	def _make_customer_record(name):
		record = models.Customer(name=name, orders=[])
		created_records.append(record)
		return record

	yield _make_customer_record

	for record in created_records:
		record.destroy()

def test_customer_records(make_customer_record):
	customer_1 = make_customer_record("Lisa")
	customer_2 = make_customer_record("Mike")
	customer_3 = make_customer_record("Meredith")
```

fixture의 매개 변수화
---
fixture 함수는 매개 변수화 될 수 있습니다. 이 경우 이 fixture 함수에 종속적인 test같이 종속적인 테스트 세트를 실행할 때 마다 여러 번 호출됩니다. 테스트 함수는 일반적으로 재실행을 인시갛지 않아도 됩니다. fixture 매개 변수화는 여러 가지 방법으로 구성할 수 있는 구성 요소에 대한 철저한 기능 테스트를 작성하는 데 도움이 됩니다.

앞의 예제를 확장하면, fixture에 플래그를 붙여 두개의 `smtp_connection` fixture 인스턴스를 생성 할 수 있습니다. 이 인스턴스는 fixture를 사용하는 모든 테스트가 두 번 실행되도록 합니다. fixture 함수는 특별한 요청 객체를 통해 각 매개 변수에 접근합니다.
```
$ pytest -q test_module.py
FFFF 								[100%]
=============================== FAILURES ===============================
______________________ test_ehlo[smtp.gmail.com] _______________________
smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_ehlo(smtp_connection):
		response, msg = smtp_connection.ehlo()
		assert response == 250
		assert b"smtp.gmail.com" in msg
> 		assert 0 # for demo purposes
E 		assert 0

test_module.py:6: AssertionError
______________________ test_noop[smtp.gmail.com] _______________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_noop(smtp_connection):
		response, msg = smtp_connection.noop()
		assert response == 250
> 		assert 0 # for demo purposes
E 		assert 0

test_module.py:11: AssertionError
______________________ test_ehlo[mail.python.org] ______________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_ehlo(smtp_connection):
		response, msg = smtp_connection.ehlo()
		assert response == 250
> 		assert b"smtp.gmail.com" in msg
E 		AssertionError: assert b'smtp.gmail.com' in b'mail.python.
˓→org\nPIPELINING\nSIZE 51200000\nETRN\nSTARTTLS\nAUTH DIGEST-MD5 NTLM CRAM-
˓→MD5\nENHANCEDSTATUSCODES\n8BITMIME\nDSN\nSMTPUTF8\nCHUNKING'

test_module.py:5: AssertionError
------------------------ Captured stdout setup -------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef>
______________________ test_noop[mail.python.org] ______________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

	def test_noop(smtp_connection):
		response, msg = smtp_connection.noop()
		assert response == 250
> 		assert 0 # for demo purposes
E 		assert 0

test_module.py:11: AssertionError
----------------------- Captured stdout teardown -----------------------
finalizing <smtplib.SMTP object at 0xdeadbeef>
4 failed in 0.12 seconds
```
우리는 두개의 테스트 함수가 각각 다른 `smtp_connection` 인스턴스에 대해 두 번 실행되었음을 알 수 있습니다. `mail.python.org` 연결을 사용하면 도착한 것 보다 다른 서버 문자열이 예상되므로 `test_ehlo`에서 두 번째 테스트가 실패합니다.

pytest는 매개 변수화 된 fixture의 각 fixture 값에 대한 테스트 ID인 문자열을 만듭니다. `test_ehlo[smtp.gmail.com]` 및 test_ehlo[mail.python.org]를 참조하십시오. 이 ID는 `-k` 와 함꼐 사용하여 실행할 특정 케이스를 선택할 수 있으며, 실패 할 경우 특정 케이스를 식별합니다. `--collect-only`로 pytest를 실행하면 생성 된 ID가 표시됩니다.

숫자, 문자열, bool 및 None은 테스트 ID에 사용 된 일반적인 문자열 표현을 갖습니다. 다른 객체의 경우 pytest는 인수 이름을 기반으로 문자열을 만듭니다. `ids` 키워드 인수를 사용하여 특정 fixture 값에 대한 테스트 ID에 사용된 문자열을 사용자 정의 할 수 있습니다.
```
# content of test_ids.py
import pytest

@pytest.fixture(params=[0, 1], ids=["spam", "ham"])
def a(request):
	return request.param

def test_a(a):
	pass

def idfn(fixture_value):
	if fixture_value == 0:
		return "eggs"
	else:
		return None

@pytest.fixture(params=[0, 1], ids=idfn)
def b(request):
	return request.param
def test_b(b):
	pass
```
위의 코드는 어떻게 `ids`가 fixture 값으로 사용하고자 하는 문자열의 리스트나 fixture 값으로 호출 될 함수의 리스트가 될 수 있는 지를 보여줍니다. 그런 다음 사용할 문자열을 반환해야 합니다. 후자의 경우 함수가 None을 반환하면 pytest의 자동 생성 ID가 사용됩니다.

위의 테스트를 실행하면 다음과 같은 테스트 ID가 사용됩니다.
```
$ pytest --collect-only
========================= test session starts ==========================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 10 items
<Module test_anothersmtp.py>
	<Function test_showhelo[smtp.gmail.com]>
	<Function test_showhelo[mail.python.org]>
<Module test_ids.py>
	<Function test_a[spam]>
	<Function test_a[ham]>
	<Function test_b[eggs]>
	<Function test_b[1]>
<Module test_module.py>
	<Function test_ehlo[smtp.gmail.com]>
	<Function test_noop[smtp.gmail.com]>
	<Function test_ehlo[mail.python.org]>
	<Function test_noop[mail.python.org]>

===================== no tests ran in 0.12 seconds =====================
```
