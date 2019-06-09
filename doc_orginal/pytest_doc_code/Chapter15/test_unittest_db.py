import unittest
import pytest

@pytest.mark.usefixtures("db_class")
class MyTest(unittest.TestCase):
	def test_method1(self):
		assert hasattr(self, "db")
		assert 0, self.db # fail for demo purposes

	def test_method2(self):
		assert 0, self.db # fail for demo purposes

