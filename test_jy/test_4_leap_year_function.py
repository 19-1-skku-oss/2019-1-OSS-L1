def test_leap_year(year):
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
	# Python program to check if the input year is a leap year or not



	# To get year (integer input) from the user
	# year = int(input("Enter a year: "))



def test_run():
	  assert test_leap_year(2000) == 1
	  assert test_leap_year(2001) == 1
	  assert test_leap_year(2002) == 1



