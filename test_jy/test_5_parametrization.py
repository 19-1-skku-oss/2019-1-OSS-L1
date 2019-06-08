import pytest

def check_leap_year(year):
	if (year % 4) == 0:
	   if (year % 100) == 0:
	       if (year % 400) == 0:
		  return 1; 
	       else:
		  return 0;
	   else:
	       return 1;
	else:
	   return 0;

@pytest.mark.parametrize('year', [2000, 2001, 2002])
def test_run(year):
    assert check_leap_year(year) == 1
