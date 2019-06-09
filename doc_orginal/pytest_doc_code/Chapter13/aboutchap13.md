내장 된 pytest.mark.parametrize 데코레이터는 테스트 함수에 대한 인수의 매개 변수화를 가능하게 만든다.

test_expectation.py에 보면 @parametrize 데코레이터는 세 개의 다른 (test_input, expected) 튜플을 정의하여
test_eval 함수를 차례로 사용하여 세번 실행한다.
