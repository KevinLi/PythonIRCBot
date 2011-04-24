#!/usr/bin/env python

__author__ = "KevinLi @ https://github.com/KevinLi"
__version__ = "0.0.1.0"

import socket

class IRC(object):
	def __init__(self, host, port, owners):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.isConnected = False
		
		self.host = host
		self.port = port
		
		self.owners = owners
		
	def createConnection(self, nick, ident, name, *password):
		self.socket.connect((self.host, self.port))
		self.isConnected = True
		self.recv()
		self.identify(nick, ident, name, password)
		self.nick = nick
		
	def identify(self, nick, ident, name, password):
		self.sendRaw("USER {0} * * :{1}".format(ident, name))
		self.sendRaw("NICK :{0}".format(nick))
		if password:
			self.sendMsg("NICKSERV", "IDENTIFY {0}".format(password[0]))
		
		
	def sendRaw(self, data):
		if self.isConnected:
			self.socket.send("{0}\r\n".format(data))
		else:
			print("Not connected.")
		
	def sendMsg(self, location, data, *action): 
		if self.isConnected:
			if action:
				if action[0]== "ACTION":
					self.sendRaw("PRIVMSG {0} :\x01ACTION {1}\x01".format(location, data))
			else:
				self.sendRaw("PRIVMSG {0} :{1}".format(location, data))
		else:
			print("Not connected.")
		
	def recv(self):
		return self.socket.recv(512)
		
	def ping(self):
		self.sendRaw("PONG :{0}".format(self.host))
	
	def returnNick(self):
		return self.nick
	
	def shutdown(self, code):
		self.socket.shutdown(code)
