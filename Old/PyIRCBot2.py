#!/usr/bin/env python
'''
Tested on Python versions 2.6.6 and 2.7.1.
'''
from __future__ import print_function
import socket
import time

version = "PyIRCBot v2.0.0"

selfNick = "" # Nick name. Name shown in an IRC channel. Max 30 char UnrealIRCd
selfIdent = "" # User name 
selfName = "" # Real name

network = "" # Network name. Ex: irc.freenode.net
port = 6667 # Port to connect to. Usually 6667 for non-SSL.
password = "" # NickServ password of the bot, if it's registered.
ircChannel = '' # Channel to join upon run.

# Users allowed to administrate the bot. Syntax: "nick":"host"
adminNicks = {
    "":"",
}
# Prohibits use of certain commands from these nicknames. For now, only CTCP.
ignoreNicks = [
    "",
]

def sendRaw(data):
    irc.send("{0}\n".format(data))
    
def sendMsg(data):
    irc.send("PRIVMSG {0} :{1}\n".format(location, data))
    
def recvParse():
    global host, nick, action, location, text
    
    msgSplit = recvData.split()
    try:
        if msgSplit[0] == "PING":
            sendRaw("PONG :{0}".format(network))
            text = ["  "," "," "," "]
        elif msgSplit[1] == "KICK" and msgSplit[3] == selfNick:
            sendRaw("JOIN {0}".format(msgSplit[2]))
            text = ["  "," "," "," "]
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
                if location.lower() == selfNick.lower():
                    location = nick
            except:
                location = " "
            # Messages received are case sensitive!
            [ text.append(i) for i in msgSplit[3:] ]
            if not text or text[0] == ":":
                text = ["  "," "," "," "]
            text[0] = text[0][1:]
    except:
        text = ["  "," "," "," "]
    
if __name__ == '__main__':
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        irc.connect((network, port))
    except:
        print("Could not connect.")
        quit()
    
    sendRaw("USER {0} * * {1}".format(selfIdent, selfName))
    sendRaw("NICK {0}".format(selfNick))
    if password:
        sendRaw("MSG NICKSERV IDENTIFY {0}".format(password))
    if ircChannel:
        sendRaw("JOIN {0}".format(ircChannel))
    
    while True:
        text = []

        try: recvData = irc.recv(1024)
        except: quit()
        print(recvData, end="")
        recvParse()
        
        # CTCP
        if text[0][0] == "\x01" and text[0][-1] == "\x01" and nick not in ignoreNicks:
            if text[0][1:-1] == "VERSION":
                sendMsg(version)
            if text[0][1:-1] == "TIME":
                sendMsg(time.ctime())
        
        # Commands allowed only to bot admins
        if nick in adminNicks and adminNicks[nick] == host:
            if action == "INVITE":
                sendRaw("JOIN :{0}".format(text[0]))
            # Customise these to personal preference.
            # Joining a channel with a comma in the channel name parts the user
            # from all channels.
            if text[0] == "join" and "," not in text[1]:
                try: sendRaw("JOIN :{0}".format(text[1]))
                except: pass
            # Change "part" to desired parting command. Same with "join", etc.
            if text[0] == "part":
                try: sendRaw("PART :{0}".format(text[1]))
                except: sendRaw("PART :{0}".format(location))
            if text[0] == "sr":
                sendRaw(" ".join(text[1:]))
            if text[0] == "quit":
                sendRaw("QUIT !")
                time.sleep(1)
                irc.shutdown(2)
                quit()
            
        # Sample public command. Add your own!
        if text[0] == "hello":
            sendMsg("hello, {0}".format(nick))