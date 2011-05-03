import IRC
import IRCParser

import time

__author__ = "KevinLi @ https://github.com/KevinLi"
__version__ = "0.0.2.0"


class IRCBot(object):
	def __init__(self, host, port, owners, channel, nick, user, name, *password):
		self.host = host
		self.port = port
		
		self.owners = owners
		self.channel = channel
		
		self.nick = nick
		self.user = user
		self.name = name
		
		self.password = password
		
	def run(self):
		Connection = IRC.IRC(self.host, self.port, self.owners)

		Connection.createConnection(self.nick, self.user, self.name, self.password)
		Connection.sendRaw("MODE {0} +B".format(Connection.nick))
		Parser = IRCParser.IRCParser()
		time.sleep(2)
		Connection.sendRaw("JOIN #{0}".format(self.channel))
		
		while True:
			try:
				recvData = Connection.recv(512)
			except:
				quit()
			print(recvData)
			data = Parser.parseMsg(recvData)
			print(data)
			
			if data[0] == "\r\n":
				pass
			elif data[0] == "PING":
				Connection.ping()
			elif data[1] == ":Closing":
				Connection.shutdown(2)
				quit
			else:
				nick = data[0][0]
				action = data[1]
				text = data[3]
				location = data[2]
				
				if not text:
					text = [" "]	
				if not text[0]:
					text[0] = " "
				
				# CTCP
				if text[0][0] == "\x01" and text[0][-1] == "\x01":
					if data[3][0][1:-1] == "VERSION":
						Connection.sendMsg(location, __version__)
					if data[3][0][1:-1] == "TIME":
						Connection.sendMsg(location, time.ctime())
					
				if nick in Connection.owners and Connection.owners[nick] == data[0][2]:
					if action == "INVITE":
						Connection.sendRaw("JOIN :{0}".format(text[0]))
					if text[0] == "join" and "," not in text[1]:
						try: Connection.sendRaw("JOIN :{0}".format(text[1]))
						except: pass
					if text[0] == "part":
						try: Connection.sendRaw("PART :{0}".format(text[1]))
						except: Connection.sendRaw("PART :{0}".format(location))
					if text[0] == "sr":
						Connection.sendRaw(" ".join(text[1:]))
					if text[0] == "!me":
						joinedText = " ".join(text[1:])
						Connection.sendMsg(location, joinedText, "ACTION")
					if text[0] == "!quit":
						Connection.sendRaw("QUIT !")
						time.sleep(1)
						Connection.shutdown(2)
						quit()
					if text[0] == "add":
						Connection.addOwner(text[1], Connection.whois(text[1]))
						Connection.sendMsg(location, "{0} added to owners list.".format(text[1]))
					if text[0] == "rm":
						Connection.rmOwner(text[1])
						Connection.sendMsg(location, "{0} removed from list.".format(text[1]))
		
				# Note to self: text[] is case sensitive.
				if text[0] == "trigger": Connection.sendMsg(location, "response")

if __name__ == '__main__':
	
	Bot = IRCBot(
		"hostname",
		port,
		{
			# "owner's nick":"owner's hostmask"
		},
		"bot's nick",
		"bot's username",
		"bot's name",
		"bot's password" # if no password, omit argument.
	)
	Bot.run()
