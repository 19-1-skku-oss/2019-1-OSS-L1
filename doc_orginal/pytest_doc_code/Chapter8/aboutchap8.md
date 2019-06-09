base temporary directory에서 만든 tmp_path로 테스트 호출에 고유한 임시 디렉토리를 제공한다.
test_tmp_path.py를 실행해 보면, 값을 확인하는데 사용하는 마지막 assert 0 제외하고 통과된 테스트 결과를 보여준다.

base temporary directory에서 만든 tmpdir로 테스트 호출에 고유한 임시 디렉토리를 제공합니다.
tmpdir는 py.path.local 개체이며 os.path 메소드 등을 제공한다.
