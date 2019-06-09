test_example을 pytest를 실행했을때, AssertionError를 알려준다. 

pytest -r 는 단순한 정보를 표시한다.

-r에 a를 붙이면(-ra) "all except passes"라는 뜻이다. 
a대신에 다른 character도 입력할 수 있다:
• f - failed
• E - error
• s - skipped
• x - xfailed
• X - xpassed
• p - passed
• P - passed with output
• a - all except pP
• A - all
