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
from Ordonnancer import Ordonnancer

from testBrick import * 

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
	
	def testGetIn(self):
		self.assertIsNone(self.brick2.GetIn(0), "Test GetIn didnt returned None with an empty IN")
		self.assertRaises(Exception, self.brick2.GetIn, 1)
		self.brick2.SetIn(0, self.buf)
		self.assertIsInstance(self.brick2.GetIn(0), Buffer, "Test GetIn didnt returned a Buffer object")
		
	def testGetOut(self):
		self.assertIsNone(self.brick1.GetOut(0), "Test GetOut didnt returned None with an empty OUT")
		self.assertRaises(Exception, self.brick1.GetOut, 1)
		self.brick1.SetOut(0, self.buf)
		self.assertIsInstance(self.brick1.GetOut(0), Buffer, "Test GetOut didnt returned a Buffer object")
	
class BrickExecutionTest(unittest.TestCase):
    def setUp(self):
        self.brick = Brick(1, 1)
    def testDoCycle(self):
        self.assertRaises(Exception, self.brick.DoCycle)

class BufferConnectionTest(unittest.TestCase):
	def setUp(self):
		self.brick1 = Brick(0, 1)
		self.brick2 = Brick(0, 1)
		self.brick3 = Brick(1, 0)
		self.brick4 = Brick(1, 0)
		self.buf = Buffer()
	def testConnectToAlreadyConnectedBufferEntry(self):
		self.brick1.SetOut(0, self.buf)
		self.assertRaises(Exception, self.brick2.SetOut, 0, self.buf)

class OrdonnancerUnitTest(unittest.TestCase):
	def setUp(self):
		self.ordo = Ordonnancer()
		self.brick1 = testBrickOut(0, 1)
		self.brick2 = testBrickIn(1, 0)
		self.buf = Buffer()
		self.brick1.SetOut(0, self.buf)
		self.brick2.SetIn(0, self.buf)
	
	def tearDown(self):
		Ordonnancer.Remove()
	
	def testAddBrick(self):
		self.assertRaises(Exception, self.ordo.AddBrick, 0)
		self.ordo.AddBrick(self.brick1)
		self.assertRaises(Exception, self.ordo.AddBrick, self.brick1)
	
	def testDoCycle(self):
		self.ordo.AddBrick(self.brick2)
		self.ordo.AddBrick(self.brick1)
		self.ordo.Run(10)

if __name__ == '__main__':
    unittest.main()
