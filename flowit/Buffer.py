from collections import deque

class Buffer:
	__idCount = 0
	def __init__(self, maxdata = 1):
		self._maxdata = maxdata
		self._id = Buffer.__idCount
		self.__connectionId = 0
		Buffer.__idCount += 1
		self._inId = -1
		self._outCtxIds = {}
		self._datas = []
	
	def __getConnectionId(self, cur_id):
		tmp = self.__connectionId
		self.__connectionId += 1
		return "%d_%d_%d" % (self._id, cur_id, tmp)
	
	def PushData(self, cur_id, data):
		if cur_id is not self._inId:
			raise Exception("Wrong Id(%d) in Buffer PushData (Buffer %d)" % (cur_id, self._id))
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

	def needData(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
			
	def isEmpty(self, cur_id):
		if cur_id not in self._outCtxIds:
			raise Exception("This ConnectionId (%d) isnt connected to that Buffer (Buffer %d)" % (cur_id, self._id))
		return (len(self._datas) - self._outCtxIds[cur_id]) == 0
	
	def isFull(self, cur_id):
		if cur_id is not self._inId:
			raise Exception("Wrong Id(%d) in Buffer isFull (Buffer %d)" % (cur_id, self._id))
		return len(self._datas) == self._maxdata
			
	def setIn(self, cur_id):
		if self._inId is not -1:
			raise Exception("Cant connect %d as Input of Buffer, already connected (Buffer %d)" % (cur_id, self._id))
		self._inId = cur_id

	def setOut(self, cur_id):
		ret = self.__getConnectionId(cur_id)
		self._outCtxIds[ret] = 0
		return ret
		
	def clean(self):
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