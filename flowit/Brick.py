from Buffer import Buffer

class Brick:
	__idCount = 0
	def __init__(self, nbIns, nbOuts):
		self._id = Brick.__idCount
		Brick.__idCount += 1
		self.__nbIns = nbIns
		self.__nbOuts = nbOuts
		self._ins = {}
		self._outs = {}
		
	def GetId(self):
		return self._id
	
	def SetIn(self, inNumber, buffer):
		if inNumber >= self.__nbIns or inNumber < 0:
			raise Exception("Cannot set %d Input Buffer (Brick %d)" % (inNumber, self._id))
		if inNumber in self._ins:
			raise Exception("%d Output already connected (Brick %d)" % (inNumber, self._id))
		if not isinstance(buffer, Buffer):
			raise Exception("Cannot connect a non Buffer object (Brick %d)" % (self._id))
		tmpId = buffer.SetOut(self._id)
		self._ins[inNumber] = [tmpId, buffer]
		
	
	def SetOut(self, outNumber, buffer):
		if outNumber >= self.__nbOuts or outNumber < 0:
			raise Exception("Cannot set %d Output Buffer (Brick %d)" % (outNumber, self._id))
		if outNumber in self._outs:
			raise Exception("%d Output already connected (Brick %d)" % (outNumber, self._id))
		if not isinstance(buffer, Buffer):
			raise Exception("Cannot connect a non Buffer object (Brick %d)" % (self._id))
		buffer.SetIn(self)
		self._outs[outNumber] = buffer
		
	def DoCycle(self):
		raise Exception("This brick havent got DoCycle Defined!!! (Brick %d)" % (self._id))
		return True
		
	def GetOut(self, outNumber):
		if outNumber >= self.__nbOuts or outNumber < 0:
			raise Exception("Cannot get %d Output Buffer (Brick %d)" % (outNumber, self._id))
		if outNumber not in self._outs:
			return None
		return self._outs[outNumber]
	
	def GetIn(self, inNumber):
		if inNumber >= self.__nbIns or inNumber < 0:
			raise Exception("Cannot get %d Input Buffer (Brick %d)" % (inNumber, self._id))
		if inNumber not in self._ins:
			return None
		return self._ins[inNumber][1]
		
	def GetNbIn(self):
		return self.__nbIns
		
	def GetNbOut(self):
		return self.__nbOuts