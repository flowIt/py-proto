import random
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

class testBrickIn(Brick):
	def DoCycle(self):
		ret = True
		for i in range(self.GetNbIn()):
			if i in self._ins:
				if self._ins[i][1].IsEmpty(self._ins[i][0]):
					if self._ins[i][1].NeedData(self._ins[i][0]) is False:
						ret = False
		if ret is True:
			print "Brick %d===================="  % (self._id)
			for i in range(self.GetNbIn()):
				if i in self._ins:
					if self._ins[i][1].IsEmpty(self._ins[i][0]) is False:
						tmp = self._ins[i][1].PopData(self._ins[i][0])
						print "Buffer %d:" % i
						print tmp
			print "============================"
		return ret
		
class testBrickOut(Brick):
	tmp = 0
	def DoCycle(self):
		ret = True
		print "Brick %d====================" % (self._id)
		for i in range(self.GetNbOut()):
			if i in self._outs:
				if self._outs[i].IsFull(self) is False:
					tmp = testBrickOut.tmp
					testBrickOut.tmp += 1
					print "Push %d in %d" % (tmp, i)
					self._outs[i].PushData(self, tmp)
		print "============================"
		return ret