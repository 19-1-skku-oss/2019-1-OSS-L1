import pytest
import time

def expensive_computation():
	print("running expensive computation...")

@pytest.fixture
def mydata(request):
	val = request.config.cache.get("example/value", None)
	if val is None:
		expensive_computation()
		val = 42
		request.config.cache.set("example/value", val)
	return val

def test_function(mydata):
	assert mydata == 23