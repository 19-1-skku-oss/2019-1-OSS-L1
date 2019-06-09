테스트 함수는 fixture 객체를 매개 변수로 받을 수 있다. 각 매개 변수 이름에 대해 그 이름을 가진 fixture 함수는 fixture 객체를 제공한다. 
fixture 함수는 @pytest로 표시되어 등록됩니다. 아래 코드는 test 모듈을 포함한 fixture, test 함수의 간단한 예시한다.


여기서 test_ehlo 는 stmp_connection fixture 값을 필요하다. pytest는 @pytest가 표시된 같은 함수를 찾아서 호출한다.

test_module.py 코드에 무슨 일이 일어나고 있는지 조사하기 위해 assert 0 를 일부로 넣는다.

pytest.param()은 @pytest.mark.parametrize와 같이 매개 변수화 된 fixture 값 세트에 표시를 하는데 사용할 수 있다.
test_fixture_marks.py에 테스트를 실행 하면 값이 2인 data_set 호출을 건너 뚼다.

test_appsetup.py에 이전의 정의 된 smtp_connection fixture를 받아 와서 App 객체를 인스턴스화 하는 app fixture를 선언한다.








