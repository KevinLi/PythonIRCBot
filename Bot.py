import IRC
import IRCParser



__author__ = "KevinLi @ https://github.com/KevinLi"
__version__ = "0.0.1.0"


if __name__ == '__main__':
	Connection = IRC.IRC("", 6667,{
                "owner nick":"owner host",
		}
        )
	Connection.createConnection("nickname", "ident", "username","password")
	Connection.sendRaw("MODE {0} +B".format(Connection.nick))
	Parser = IRCParser.IRCParser()
	time.sleep(2)
	Connection.sendRaw("JOIN #channel")
	
	while True:
		try:
			recvData = Connection.recv()
		except:
			quit()
			
		data = Parser.parseMsg(recvData)
		print(data)
		
		nick = data[0][0]
		
		if data[0] == "\r\n":
			pass
		elif data[0] == "PING":
			Connection.sendRaw("PONG {0}".format(data[1]))
		else:
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
					Connection.sendMsg(__version__)
				if data[3][0][1:-1] == "TIME":
					Connection.sendMsg(time.ctime())
				
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
					sendData = ""
					Connection.sendRaw(" ".join(text[1:]))
				if text[0] == "quit":
					Connection.sendRaw("QUIT !")
					time.sleep(1)
					Connection.shutdown(2)
					quit()
	
			# Note to self: text[] is case sensitive.
			if text[0] == "trigger": Connection.sendMsg(location, "response")
			
