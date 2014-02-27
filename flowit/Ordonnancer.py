import copy

class Ordonnancer:
	__instance = None
	
	@classmethod
	def Remove(cls):
		cls.__instance = None
	@classmethod	
	def GetInstance(cls):
		if cls.__instance is None:
			cls.__instance = Ordonnancer()
		return cls.__instance

	def __init__(self):
		if Ordonnancer.__instance is not None:
			raise Exception("There is already an ordonnancer RDY!")
		Ordonnancer.__instance = self
		self._bricks = []
		self._tmp = []
		self._todo = []
		self._needData = []
		self._done = []
	
	def AddBrick(self, brick):
		from Brick import Brick
		if not isinstance(brick, Brick):
			raise  Exception("You are adding something that is not a brick into the ordonnacer")
		if brick in self._bricks:
			raise Exception("You are adding a Brick Twice!")
		self._bricks.append(brick)
		
		
	def Run(self, maxcycle = 0):
		cyclenum = 0
		self._done = copy.copy(self._bricks)
		while maxcycle == 0 or cyclenum < maxcycle:
			print "=================CYCLE %d=====================" % cyclenum
			self._tmp = self._done
			self._needData = []
			self._todo = []
			self._done = []
			while True:
				if len(self._needData):
					while len(self._needData):
						tmp = self._needData[0]
						del self._needData[0]
						if tmp.DoCycle() is True:
							self._done.append(tmp)
						else:
							self._todo.insert(0, tmp)
				elif len(self._todo):
					while len(self._todo):
						if self._todo[0].DoCycle() is True:
							self._done.append(self._todo[0])
							del self._todo[0]
						else:
							break
				elif len(self._tmp):
					while len(self._tmp):
						tmp = self._tmp[0]
						del self._tmp[0]
						if tmp.DoCycle() is True:
							self._done.append(tmp)
						else:
							self._todo.insert(0, tmp)
							break
				else:
					break
			cyclenum += 1
	
	def PushNeedData(self, brick):
		print "======ORDONNANCER NEEDDATA For %d=========" % brick.GetId()
		try:
			i = self._needData.index(brick)
			del self._needData[i]
			print "UPPING IN NEEDDATA"
			self._needData.insert(0, brick)
			print "======ORDONNANCER NEEDDATA False========="
			return False
		except:
			pass
		try:
			i = self._tmp.index(brick)
			del self._tmp[i]
			print "INSERTING IN NEEDDATA %d" % brick.GetId()
			self._needData.insert(0, brick)
			print "======ORDONNANCER NEEDDATA False========="
			return False
		except:
			pass
		print "======ORDONNANCER NEEDDATA True========="	
		return True