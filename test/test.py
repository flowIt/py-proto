import sys
import os
import inspect
import unittest

# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
   
# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../flowit")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

from Brick import Brick
from Buffer import Buffer

class BrickConnectionTest(unittest.TestCase):
    def setUp(self):
        self.brick1 = Brick(0, 1)
        self.brick2 = Brick(1, 0)
        self.brick3 = Brick(1, 0)
        self.buf = Buffer()
    def testConnectToUnexistingBrickEntry(self):
        self.assertRaises(Exception, self.brick1.SetIn, 0, self.buf)
    def testConnectToAlreadyConnectedBrickEntry(self):
        self.brick2.SetIn(0, self.buf)
        self.assertRaises(Exception, self.brick2.SetIn, 0, self.buf)
    def testConnectSomethingElseThanBuffer(self):
        self.assertRaises(Exception, self.brick2.SetIn, 0, 0)

class BrickExecutionTest(unittest.TestCase):
    def setUp(self):
        self.brick = Brick(1, 1)
    def testDoCycle(self):
        self.assertRaises(Exception, self.brick.DoCycle)

if __name__ == '__main__':
    unittest.main()
