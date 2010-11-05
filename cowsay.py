#! usr/bin/env python
"""
Program: Cowsay
Version: 1.0.3.28
Author: Kevin/banhammer
Editors: Cam

Description: CowBot is a bot designed to send different ascii cows and text to an IRC channel
"""

import socket
import sys
from time import sleep

#irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc = socket.socket()
network = ''
port = 6667
ircchannel = '#'

ircname = 'Cowsay' # max 30 characters
realname = 'COWSAYBOT'
ident = 'cows'
password = ''

crlf = '\r\n'
onoff = 'on'
cow = True

admins = []
allowedhosts = []

def SendIRCRaw(rawtext):
    irc.send(rawtext+crlf)
    
def SendText(text):
    irc.send("PRIVMSG {0} :{1}".format(location, text) + crlf)

def SendPM(text):
    irc.send("PRIVMSG {0} :{1}".format(nick, text) + crlf)
    
def CowIsOff():
    SendText("Cowsay is off.")

irc.connect((network, port))
SendIRCRaw("NICK {0}".format(ircname))
SendIRCRaw("USER {0} **** **** :{1}".format(ident, realname))
sleep(1)
SendIRCRaw("NickServ IDENTIFY {0}".format(password))
SendIRCRaw("MODE {0} +B".format(ircname))
sleep(1)
SendIRCRaw("JOIN %s" % ircchannel)

# [0]host, [1]channel, [2]nick, [3+]message
while True:
# Parse Message --------------------------------------------    
        msg = irc.recv(512)
        msgsplit = msg.split()
        print(msg)
        if len(msg.split())>0:
            if msg.split()[0] == "PING":
                SendIRCRaw("PONG %s" % msg.split()[1])
#        if len(msg.split())>1:
#            if msg.split()[1] == "001":
#                print("001")
#                SendIRCRaw("JOIN %s" % ircchannel)
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
        cowsaylog = open("cowsaylog.txt",'a')
#        cowsaylog.write(str(nick+"\t"+host+"\t"+location+"\t"+cmd+"\t"+text)+"\n")
        cowsaylog.write(msg)
# Ignore PMs -----------------------------------------------

# Admin Commands -------------------------------------------
        if nick in admins:
            if host in allowedhosts:
                if cmd == "cow":
                    onoff = " ".join(msg.split()[3:][1:])
                    if onoff == "off":
                        cow = False
                        SendIRCRaw("NOTICE {0} COW OFF".format(nick))
                    if onoff == "on":
                        cow = True
                        SendIRCRaw("NOTICE {0} COW ON".format(nick))
                if cmd == "part":
                    SendIRCRaw("PART :#" + msg.split()[4])
                if cmd == "join":
                    SendIRCRaw("JOIN :#" + msg.split()[4])
                if cmd == "cowshit":
                    SendIRCRaw("QUIT MOO")
                    quit()
                if cmd == "status":
                    SendPM(onoff)
                if cmd == "sendraw":
                    SendIRCRaw(" ".join(msg.split()[3:][1:]))
# Cows -----------------------------------------------------
        c = " ".join(msg.split()[3:][1:])
        cnum = int(len(c))
        cdash = cnum*"_"
        cdash2 = cnum*"-"
        def say_beginning(cdash,c,cdash2):
            SendText(" _{0}_".format(cdash))
            SendText("< {0} >".format(c))
            SendText(" -{0}-".format(cdash2))
        def thought_beginning(cdash,c,cdash2):
            SendText(" _{0}_".format(cdash))
            SendText("( {0} )".format(c))
            SendText(" -{0}-".format(cdash2))
        if cow is True:
            if cmd == "cowsay":
                say_beginning(cdash,c,cdash2)
                SendText("        \   ^__^")
                SendText("         \  (oo)\_______")
                SendText("            (__)\       )\/\ ")
                SendText("                ||----w |")
                SendText("                ||     ||")
            if cmd == "cowdrunk":
                say_beginning(cdash,c,cdash2)
                SendText("        \   ^__^")
                SendText("         \  (**)\_______")
                SendText("            (__)\       )\/\ ")
                SendText("             U  ||----w |")
                SendText("                ||     ||")
            if cmd == "cowsex":
                say_beginning(cdash,c,cdash2)
                SendText("      \                _")
                SendText("       \              (_)")
                SendText("        \   ^__^       / \ ")
                SendText("         \  (oo)\_____/_\ \ ")
                SendText("            (__)\       ) /")
                SendText("                ||----w ((")
                SendText("                ||     ||>> ")
            if cmd == "tux":
                SendIRCRaw("NICK Penguin")
                sleep(1)
                thought_beginning(cdash,c,cdash2)
                SendText("   o    .--.")
                SendText("    o  |o_o |")
                SendText("       |:_/ |")
                SendText("      //   \\ \\")
                SendText("     (|     | )")
                SendText("    /'\\_   _/`\\")
                SendText("    \\___)=(___/")
                SendIRCRaw("NICK Cow")

# Cow Off Notification -------------------------------------
        elif cmd == "cowsay":
            CowIsOff()
        elif cmd == "cowdrunk":
            CowIsOff()
        elif cmd == "cowsex":
            CowIsOff()
        elif cmd == "tux":
            CowIsOff()
# Public Commands ------------------------------------------
        if cmd == "cowhelp":
            SendPM("Available commands are:")
            SendPM("cowhelp          status")
            SendPM("cow on/off      cowshit")
            SendPM("cowjoin         cowpart")
            SendPM("-----------------------")
            SendPM("cowsay         cowdrunk")
            SendPM("cowsex")
        if cmd == "no":
            nou = " ".join(msg.split()[3:][1:])
            if nou == "U":
                SendText("NO U")
            if nou == "YOU":
                SendText("NO YOU")
        if cmd == "beef":
            beef_for = " ".join(msg.split()[3:][1:])
            SendIRCRaw("PRIVMSG {0} :\x01ACTION cooks up some fancy steak for {1}.\x01".format(location, beef_for))
