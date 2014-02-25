from collections import deque
from Ordonnancer import Ordonnancer

class Buffer:
	__idCount = 0
	def __init__(self, maxdata = 1):
		self._maxdata = maxdata
		self._id = Buffer.__idCount
		self.__connectionId = 0
		Buffer.__idCount += 1
		self._inBrick = None
		self._outCtxIds = {}
		self._datas = []
	
	def __getConnectionId(self, cur_id):
		tmp = self.__connectionId
		self.__connectionId += 1
		return "%d_%d_%d" % (self._id, cur_id, tmp)
	
	def PushData(self, brick, data):
		if brick is not self._inBrick:
			raise Exception("Wrong Brick(%d) in Buffer PushData (Buffer %d)" % (brick.GetId(), self._id))
		self._datas.append([data, len(self._outCtxIds)])
		
	def PopData(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
		if self._outCtxIds[cur_id] >= len(self._datas):
			return None
		tmp = self._datas[self._outCtxIds[cur_id]]
		tmp[1] -= 1
		self._outCtxIds[cur_id] += 1
		return tmp[0]

	def PeekData(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
		if self._outCtxIds[cur_id] >= len(self._datas):
			return None
		return self._datas[self._outCtxIds[cur_id]][0]

	def NeedData(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
		return Ordonnancer.GetInstance().PushNeedData(self._inBrick)
			
	def IsEmpty(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
		return (len(self._datas) - self._outCtxIds[cur_id]) == 0
	
	def IsFull(self, brick):
		if brick is not self._inBrick:
			raise Exception("Wrong Brick(%d) in Buffer isFull (Buffer %d)" % (brick.GetId(), self._id))
		ret = (len(self._datas) == self._maxdata)
		if ret is True:
			self.Clean()
		return len(self._datas) == self._maxdata
			
	def SetIn(self, brick):
		if self._inBrick is not None:
			raise Exception("Cant connect %d as Input of Buffer, already connected (Buffer %d)" % (cur_id, self._id))
		self._inBrick = brick

	def SetOut(self, cur_id):
		ret = self.__getConnectionId(cur_id)
		self._outCtxIds[ret] = 0
		return ret
		
	def Clean(self):
		i = 0
		while len(self._datas):
			if self._datas[0][1] == 0:
				i += 1
				del self._datas[0]
			else:
				break
		if i > 0:
			for val in self._outCtxIds:
				self._outCtxIds[val] -= i
				if self._outCtxIds[val] < 0:
					raise Exception("A Connection(%d) value in a buffer is negative! (Buffer %d)" % (val, self._id))