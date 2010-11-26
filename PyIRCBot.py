#! usr/bin/env python
"""
Program: General purpose IRC bot
Version: 1.0.4.25
Author: Kevin
Description:
"""
# Imports ---------------
import socket
import random
import time
import urllib
# Bot details -----------
ircname = '' # max 30 characters
realname = ''
ident = ''
# Constants -------------
irc = socket.socket()
port = 6667
# Variables -------------
crlf = '\r\n'
noucounter = 0
noutoggle = 1
wat = 0
love = 0
timer = time.time()
nourand = random.randint(1,4) #random number, limit of "no u"'s
# Userlist ----
admins = []
allowedhosts = []
toignore = []
# IRC functions ---------
def SendIRCRaw(rawtext):
    irc.send(rawtext+crlf)
def SendText(text):
    irc.send("PRIVMSG {0} :{1}".format(location, text) + crlf)
def SendPM(text):
    irc.send("PRIVMSG {0} :{1}".format(nick, text) + crlf)
# Start: Settings -----------------------------------------
network = raw_input("Server (default: ): ")
if network == "":
    network = ""
password = raw_input("Password (default: none): ")
IRCChannel0 = "#" + raw_input("Channel 0 (default: #): #")
if IRCChannel0 == "#":
    IRCChannel0 = "#"
JoinChannel1 = raw_input("Join second channel? Y/N (default: N) ").lower()
if JoinChannel1 != "y": pass
else: IRCChannel1 = "#" + raw_input("Channel 1: #")
print("")

# Start: Connection ---------------------------------------
print("Connecting.")
irc.connect((network, port))
SendIRCRaw("NICK {0}".format(ircname))
SendIRCRaw("USER {0} **** **** :{1}".format(ident, realname))
time.sleep(1)
if password == '': pass
else: SendIRCRaw("NickServ IDENTIFY {0}".format(password))
SendIRCRaw("MODE {0} +B".format(ircname))
print("Bot started.")
# [0]host, [1]channel, [2]nick, [3:]message
while True:
# Parse Message -------------------------------------------
    msg = irc.recv(512)
    msgsplit = msg.split()
    if len(msg.split()) > 0:
        if msg.split()[0] == "PING":
            SendIRCRaw("PONG :{0}".format(network))
    if len(msg.split()) > 1:
        if msg.split()[1] == "372":
            SendIRCRaw("JOIN {0}".format(IRCChannel0))
            if JoinChannel1 == 'y':
                SendIRCRaw("JOIN {0}".format(IRCChannel1))
    if len(msg.split()) > 3:
        if msg.split()[1] == "KICK":
            SendIRCRaw('JOIN {0}'.format(msg.split()[2]))
    '''
    if len(msg.split()) > 2:
        if password != "":
            if msg.split()[1] == "451":
                 SendIRCRaw("MSG NickServ GHOST {0} {1}".format(ircname, password))
    '''
    if len(msg.split()) >= 4:
        try:
            host = msgsplit[0].split("@")[1]
        except:
            host = ""
        text = " ".join(msg.split()[3:][1:])
        cmd = msg.split()[3][1:].lower()
        location = msg.split()[2]
        nick = msg.split("!")[0][1:]
    else:
        cmd = ""
        location = ""
        nick = ""
        text = ""
    if msg.split()[0][1:] != "moon.n0v4.com": print(msg)
# Logging --------------------------------------------------
#   log = open("log.txt",'a')
#   log.write(str(nick+"\t"+host+"\t"+location+"\t"+cmd+"\t"+text)+"\n")
#   log.write(msg)
# Ignore PMs -----------------------------------------------

# Admin Commands -------------------------------------------
    if nick in admins:
        if host in allowedhosts:
            if msg.split()[1] == "INVITE":
                SendIRCRaw("JOIN {0}".format(cmd))
            if cmd == "[part]":
                try: SendIRCRaw("PART :#" + msg.split()[4])
                except: pass
            if cmd == "[join]":
                try: SendIRCRaw("JOIN :#" + msg.split()[4])
                except: pass
            if cmd == "[quit]":
                SendIRCRaw("QUIT I QUIT")
                quit()
            if cmd == "[sendraw]":
                SendIRCRaw(" ".join(msg.split()[3:][1:]))
            if cmd == "[cycle]":
                SendIRCRaw("PART :{0}".format(location))
                SendIRCRaw("JOIN :{0}".format(location))
            if cmd == "[reset]":
                if text == "all":
                    noutoggle = 1
                    noucounter = 0
                    nourand = random.randint(1,3)
                    wat = 0
                if text == "nou":
                    noutoggle = 1
                    noucounter = 0
                    nourand = random.randint(1,3)
                if text == "wat":
                    wat = 0
# Public Commands ------------------------------------------
    #if cmd == "@{0}help".format(ircname):
    #   SendPM("Available commands are:")
    if cmd == "wat":
        if text == "":
            if nick not in toignore:
                if wat < 2:
                    SendText("wat")
                    wat += 1
        else: pass
    if cmd == "<3":
        if love < 10:
            SendText("<3!")
            love += 1
    if cmd == "no":
        if text.lower() == "u":
            if noutoggle == 1:
                if noucounter < nourand:
                    SendText("NO U")
                    noucounter += 1 #counter, counts number of no u's sent
                elif noucounter == nourand:
                    SendText("FINE, ME")
                    noucounter += 1
                    noutoggle = 0
                else: pass
    if cmd == "meme":
        memeurl = "http://api.automeme.net/text?lines=1"
        memes = urllib.urlopen(memeurl).read().replace('\n','').replace("_","\x02")
        SendIRCRaw("PRIVMSG {0} {1}".format(location, memes))
    if cmd == "timer":
        SendText("Last reset: "+str(timer))
        SendText("Now:      "+str(time.time()))
        SendText("Next reset: "+str(timer+60))
# Time based events ----------------------------------------
    if time.time() > timer+60:
        timer = time.time() #Reset timer
        noutoggle = 1
        noucounter = 0
        nourand = random.randint(1,3)
        wat = 0
        print("Reset\n")
    else: pass
