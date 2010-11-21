#! usr/bin/env python
"""
Program: 
Version: 1.0.4.67
Author: Kevin

Description:
"""

import socket
import random
from time import sleep
import urllib

ircname = 'HerpDerp' # max 30 characters
realname = 'Hurr Durr'
ident = 'HerpDerp'

irc = socket.socket()
port = 6667

crlf = '\r\n'
noucounter = 0

admins = ["kevin","horkx3","ferus"]
allowedhosts = ["127.0.0.1","the.interwebs"]

def SendIRCRaw(rawtext):
    irc.send(rawtext+crlf)
    
def SendText(text):
    irc.send("PRIVMSG {0} :{1}".format(location, text) + crlf)

def SendPM(text):
    irc.send("PRIVMSG {0} :{1}".format(nick, text) + crlf)
    
# Start Bot
network = raw_input("Server: ")
if network = "":
    network = "earth.n0v4.com"
password = raw_input("Password: ")
ircchannel0 = "#" + raw_input("Channel 0: ")
if channel0 = "":
    ircchannel0 = "#lobby"
joinchannel1 = raw_input("Join second channel? Y/N ").lower()
if joinchannel1 != "y": pass
else: ircchannel1 = "#" + raw_input("Channel 1: ")

irc.connect((network, port))
SendIRCRaw("NICK {0}".format(ircname))
SendIRCRaw("USER {0} **** **** :{1}".format(ident, realname))
sleep(1)
if password == '':
    pass
else:
    SendIRCRaw("NickServ IDENTIFY {0}".format(password))
SendIRCRaw("MODE {0} +B".format(ircname))
sleep(1)
print("Bot started.")
# [0]host, [1]channel, [2]nick, [3+]message
while True:
# Parse Message --------------------------------------------    
    msg = irc.recv(512)
    msgsplit = msg.split()
    if len(msg.split())>0:
        if msg.split()[0] == "PING":
            SendIRCRaw("PONG {0}".format(msg.split()[1]))
    if len(msg.split())>1:
        if msg.split()[1] == "372":
            print("372")
            SendIRCRaw("JOIN {0}".format(ircchannel0))
            if joinchannel1 == 'y':
                SendIRCRaw("JOIN {0}".format(ircchannel1))
            else: pass
    if len(msg.split())>=4:
        try:
            host = msgsplit[0].split("@")[1].lower()
        except:
            host = ""
        text = " ".join(msg.split()[3:][1:])
        cmd = msg.split()[3][1:].lower()
        location = msg.split()[2]
        nick = (msg.split()[0].split("!")[0])[1:].lower()
    elif len(msg.split())>=4:
        cmd = msg.split()[4].lower()
    else:
        cmd = ""
        location = ""
        nick = ""
        text = ""
# Logging --------------------------------------------------
#    log = open("log.txt",'a')
#    log.write(str(nick+"\t"+host+"\t"+location+"\t"+cmd+"\t"+text)+"\n")
#    log.write(msg)
# Ignore PMs -----------------------------------------------

# Admin Commands -------------------------------------------
    if nick in admins:
        if host in allowedhosts:
                if cmd == ";p":
                    SendIRCRaw("PART :#" + msg.split()[4])
                if cmd == ";j":
                    SendIRCRaw("JOIN :#" + msg.split()[4])
                if cmd == "herpderp":
                    SendIRCRaw("QUIT HERP DERP")
                    quit()
                if cmd == ";sendraw":
                    SendIRCRaw(" ".join(msg.split()[3:][1:]))
                if cmd == ";cycle":
                    channelcycle = " ".join(msg.split()[3:][1:])
                    SendIRCRaw("PART :#{0}".format(channelcycle))
                    SendIRCRaw("JOIN :#{0}".format(channelcycle))
# Public Commands ------------------------------------------
    if cmd == "@{0}help".format(ircname):
        SendPM("Available commands are:")
    nourand = random.randint(1,5) #random number, limit of no u's
    if cmd == "no":
        nou = " ".join(msg.split()[3:][1:]) #second word.
        noutoggle = True #if no u is on or off
        if nou == "u":
            if noutoggle == True:
                if noucounter < nourand:
                    SendText("NO U")
                    noucounter += 1 #counter, counts number of no u's sent
                elif noucounter == nourand:
                    SendText("Fine, me.")
                    noutoggle = False
                else: pass
            else: pass
        if nou == "reset":
            noutoggle = True
            noucounter = 0
            nourand = random.randint(1,3)
    if cmd == "meme":
        memeurl = "http://api.automeme.net/text?lines=1"
        memes = urllib.urlopen(memeurl).read().replace('\n','').replace("_","\x02")
        SendIRCRaw("PRIVMSG {0} {1}".format(location, memes))
    if cmd == "oldspice":
            SendPM("Look at your comment, now back to mine.")
            SendPM("Now back at your comment, now back to mine.")
            SendPM("Sadly it isn't mine, but if you stopped trolling and started posting legitimate comments, it could look like mine.")
            SendPM("Look down, back up, where are you?")
            SendPM("You're scrolling through comments, writing the comment your comment could look like.")
            SendPM("What did you post?")
            SendPM("Back at mine, it's a reply saying something you want to hear.")
            SendPM("Look again, the reply is now diamonds.")
    try:
        a0 = cmd.split()[0][0].lower()
        a1 = cmd.split()[0][1].lower()
        a2 = cmd.split()[0][2].lower()
        alength = len(cmd.split()[0])
        a3 = str(chr(ord(a1)+1)*alength)
        a31 = ord(a1)
        if a0 == a1 == a2:
            if a31 < 96: pass
            elif a31 == 122: SendText('a'*alength)
            elif a31 > 122: pass
            else:
                try: SendText(a3)
                except IndexError: pass
    except IndexError:
        pass
