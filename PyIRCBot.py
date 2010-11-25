#! usr/bin/env python
"""
Program: General purpose IRC bot
Version: 1.0.4.20
Author: Kevin

Description:
"""

import socket
import random
import time
import urllib

ircname = '' # max 30 characters
realname = ''
ident = ''

irc = socket.socket()
port = 6667

crlf = '\r\n'
noucounter = 0
noutoggle = 1
wat = 0
timer = time.time()
nourand = random.randint(2,4) #random number, limit of "no u"'s

admins = []
allowedhosts = []

def SendIRCRaw(rawtext):
    irc.send(rawtext+crlf)
    
def SendText(text):
    irc.send("PRIVMSG {0} :{1}".format(location, text) + crlf)

def SendPM(text):
    irc.send("PRIVMSG {0} :{1}".format(nick, text) + crlf)

# Start: Settings -----------------------------------------
network = raw_input("Server (default: ): ") #edit this
if network == "":
    network = "" #default server
password = raw_input("Password (default: none): ")
IRCChannel0 = "#" + raw_input("Channel 0 (default: ): #") #edit this
if IRCChannel0 == "#":
    IRCChannel0 = "#" #default channel
JoinChannel1 = raw_input("Join second channel? Y/N (default: N) ").lower()
if JoinChannel1 != "y": pass
else: IRCChannel1 = raw_input("Channel 1: ")
print("")

# Start: Connection ---------------------------------------
print("Connecting.")
irc.connect((network, port))
SendIRCRaw("NICK {0}".format(ircname))
SendIRCRaw("USER {0} **** **** :{1}".format(ident, realname))
time.sleep(1)
if password == '':
    pass
else:
    SendIRCRaw("NickServ IDENTIFY {0}".format(password))
SendIRCRaw("MODE {0} +B".format(ircname))
print("Bot started.")
# [0]host, [1]channel, [2]nick, [3+]message
while True:
# Parse Message -------------------------------------------
    msg = irc.recv(512)
    msgsplit = msg.split()
    print(msg)
    if len(msg.split()) > 0:
        if msg.split()[0] == "PING":
            SendIRCRaw("PONG {0}".format(msg.split()[1]))
    if len(msg.split()) > 1:
        if msg.split()[1] == "372":
            SendIRCRaw("JOIN {0}".format(IRCChannel0))
            if JoinChannel1 == 'y':
                SendIRCRaw("JOIN {0}".format(IRCChannel1))
    #if len(msg.split()) > 2:
        #if password != "":
            #if msg.split()[1] == "451":
                 #SendIRCRaw("MSG NickServ ghost {0} {1}".format(ircname, password")
    if len(msg.split()) >= 4:
        try:
            host = msgsplit[0].split("@")[1].lower()
        except:
            host = ""
        text = " ".join(msg.split()[3:][1:])
        cmd = msg.split()[3][1:].lower()
        location = msg.split()[2]
        nick = (msg.split()[0].split("!")[0])[1:].lower()
    else:
        cmd = ""
        location = ""
        nick = ""
        text = ""
# Time based events ----------------------------------------
    if cmd == "timer":
        SendText(timer)
        SendText(time.time())
    if time.time() > timer+60:
        timer = time.time() #Reset timer
        noutoggle = 1
        noucounter = 0
        nourand = random.randint(1,3)
        wat = 0
        print("Reset\n")
    else: pass
# Logging --------------------------------------------------
#   log = open("log.txt",'a')
#   log.write(str(nick+"\t"+host+"\t"+location+"\t"+cmd+"\t"+text)+"\n")
#   log.write(msg)
# Ignore PMs -----------------------------------------------

# Admin Commands -------------------------------------------
    if nick in admins:
        if host in allowedhosts:
            if cmd == "[part":
                try:
                    SendIRCRaw("PART :#" + msg.split()[4])
                except: pass
            if cmd == "[join":
                try:
                    SendIRCRaw("JOIN :#" + msg.split()[4])
                except: pass
            if cmd == "herpderp":
                SendIRCRaw("QUIT HERP DERP")
                quit()
            if cmd == "[sendraw":
                SendIRCRaw(" ".join(msg.split()[3:][1:]))
            if cmd == "[cycle":
                channelcycle = " ".join(msg.split()[3:][1:])
                SendIRCRaw("PART :#{0}".format(channelcycle))
                SendIRCRaw("JOIN :#{0}".format(channelcycle))
            if cmd == "[reset":
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
        if wat < 2:
            SendText("wat")
            wat += 1
        else: pass
    if cmd == "no":
        if text == "u":
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
    try:
        alength = len(cmd.split()[0])
        a0 = cmd.split()[0][0].lower()
        a1 = cmd.split()[0][1].lower()
        a2 = cmd.split()[0][alength].lower()
        a3 = str(chr(ord(a1)+1)*alength)
        a31 = ord(a1)
        print(alength+a0+a1+a2+a3+a31)
        if a0 == a1 == a2:
            print("a0==a1==a2")
            if a31 < 96: pass
            elif a31 == 122: SendText('a'*alength)
            elif a31 > 122: pass
            else:
                try: SendText(a3)
                except IndexError: pass
    except IndexError: pass
    
