'''
This is where we put all of our test cases.
Each class is a set of tests, to test a certain thing, like a certain device, or networking.
Within each test class is sets of test functions to run. Each test starts and kills a new rov instance
'''
from rovtest import ROVTest

class TestOne(ROVTest):
    def test_upper(self):
        self.assertEqual('foo'.upper(),'FOO')

class TestTwo(ROVTest):
    def test_upper(self):
        self.assertEqual('foo'.upper(),'FOO')