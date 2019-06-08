import pytest

@pytest.fixture(scope="class")
def db_class(request):
	class DummyDB(object):
		pass
	# set a class attribute on the invoking test context
	request.cls.db = DummyDB()