#!/usr/bin/python
PKG='can_com'
import roslib; roslib.load_manifest(PKG)

import sys
import unittest

class TestUnit1(unittest.TestCase):
    def test_one(self):
        self.assertEquals(1,1,'1!=1')

if __name__ == '__main__':
    import rosunit
    rosunit.unitrun(PKG, 'unit1', TestUnit1)
