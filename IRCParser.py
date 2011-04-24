
__author__ = "KevinLi @ https://github.com/KevinLi"
__version__ = "0.0.1.0"

class IRCParser(object):
	def __init__(self):
		pass
	
	def parseMsg(self, rawData):
		if not rawData:
			raise IRCParseError("Empty line.")
		
		data = rawData.split(" ")
		
		if len(data) < 2:
			return [ data[0] ]
		if len(data) == 2 and data[0] == "PING":
			return [ data[0], data[1].replace("\r\n","") ]
			
		nick, user, host = self.parseUserInfo(data[0])
		
		text = data[3:]
		if text:
			if text[0][0] == ":":
				text[0] = text[0][1:]
			if text[-1][-2:] == "\r\n":
				text[-1] = text[-1][:-2]
		
		return [[nick, user, host], data[1], data[2], text]
		
	def parseUserInfo(self, data):
		try:
			nick = data.split("!")[0][1:]
			user = data.split("@")[0].split("!")[1]
			host = data.split("@")[1]
			return [nick, user, host]
		except:
			return ["","",""]
	
class IRCParseError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
	
