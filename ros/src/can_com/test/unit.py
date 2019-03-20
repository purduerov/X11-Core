#! /usr/bin/python
import sys
import unittest

PKG = 'can_com'

import roslib; roslib.load_manifest(PKG)



class BasicTest(unittest.TestCase):

    def test_one(self):
        self.assertEquals(1,1,'1!=1')

if __name__ == '__main__':
    import rosunit
    rosunit.unitrun(PKG, 'unit', BasicTest)
