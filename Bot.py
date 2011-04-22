import IRC
import time

__version__ = "0.0.0.1"

# Todo: Parser module?
#       Somehow remove the 'text = []'?

def recvParse():
    global host, nick, action, location, text
    
    msgSplit = recvData.split()
    try:
        if msgSplit[0] == "PING":
            Connection.ping()
            text = ["  ", " ", " ", " "]
        elif msgSplit[1] == "KICK" and msgSplit[3] == nick:
            Connection.sendRaw("JOIN {0}".format(msgSplit[2]))
            text = ["  ", " ", " ", " "]
        elif msgSplit[1] == "433":
            quit()
        else:
            try:
                host = msgSplit[0].split("@")[1]
                nick = msgSplit[0].split("!")[0][1:]
            except:
                host = nick = " "
            try:
                action = msgSplit[1]
            except:
                action = ""
            try:
                location = msgSplit[2]
                if location.lower() == nick.lower():
                    location = nick
            except:
                location = " "
            [ text.append(i) for i in msgSplit[3:] ]
            if not text or text[0] == ":":
                text = ["  ", " ", " ", " "]
            text[0] = text[0][1:]
    except:
        text = ["  ", " ", " ", " "]

if __name__ == '__main__':
    Connection = IRC.IRC("", 6667)
    Connection.createConnection("nick", "ident", "name")
    Connection.sendRaw("MODE {0} +B".format(Connection.nick))
    
    while True:
        try:
            recvData = Connection.recv()
        except:
            quit()
        print(recvData)
        text = []
        recvParse()
        
        # CTCP
        if text[0][0] == "\x01" and text[0][-1] == "\x01":
            if text[0][1:-1] == "VERSION":
                Connection.sendMsg(__version__)
            if text[0][1:-1] == "TIME":
                Connection.sendMsg(time.ctime())
            
        if nick in Connection.owners and Connection.owners[nick] == host:
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
        if text[0] == "trigger text":
            Connection.sendMsg("response")
        
