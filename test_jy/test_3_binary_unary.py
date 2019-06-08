def test_binary():
	a = 5
	b =7
	c=15
	d=-32

	print(a*d+b*c)
	print(a/b)
	print((a+d)*b*c)
	assert(a+b) == 13


def test_unary():
	a=5

	assert(-5) == -5


