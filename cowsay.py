#! usr/bin/env python
"""
Program: CowBot
Version: 9.0.0.1
Author: banhammer
Editors: Cam

Description: CowBot is a bot designed to send different ascii cows and text to an IRC channel
"""

import socket
import sys

irc = socket.socket()
network = 'irc.n0v4.com'
port = 6667
ircchannel = '#Bots'

ircname = 'Cowsay' # max 30 characters
realname = 'COWSAYBOT'
ident = 'CowsayBot'

crlf = "\r\n"
onoff = "on"
cow = True

admins = ["Banhammer","Horkx3"]
allowedhosts = ["127.0.0.1","the.interwebs"]

def SendIRCRaw(x):
    irc.send(x+crlf)
    
def SendText(text):
    irc.send("PRIVMSG %s :%s" % (location, text) + crlf)

def SendPM(text):
    irc.send("PRIVMSG %s :%s" % (nick, text) + crlf)
    
def CowIsOff():
    SendText("Cowsay is off.")

irc.connect((network, port))
SendIRCRaw("NICK %s" % ircname)
SendIRCRaw("USER %s **** **** :%s" % (ident, realname))
#sleep(3)
#SendIRCRaw("MSG NickServ IDENTIFY password")

# [0]host, [1]channel, [2]nick, [3+]message
while True:
# Parse Message --------------------------------------------    
        msg = irc.recv(512)
        msgsplit = msg.split()
        print msg
        if len(msg.split())>0:
            if msg.split()[0] == "PING":
                SendIRCRaw("PONG %s" % msg.split()[1])
        if len(msg.split())>1:
            if msg.split()[1] == "001":
                print "001"
                SendIRCRaw("JOIN %s" % ircchannel)
        if len(msg.split())>=4:
            try:
                host = msgsplit[0].split("@")[1].lower()
            except:
                host = ""
            text = " ".join(msg.split()[3:][1:])
            cmd = msg.split()[3][1:].lower()
            location = msg.split()[2]
            nick = (msg.split()[0].split("!")[0])[1:].capitalize()
        elif len(msg.split())>=4:
            cmd = msg.split()[4].lower()
        else:
            cmd = ""
            location = ""
            nick = ""
            text = ""
# Ignore PMs -----------------------------------------------

# Admin Commands -------------------------------------------
        if nick in admins:
            if host in allowedhosts:
                if cmd == "cow":
                    onoff = " ".join(msg.split()[3:][1:])
                    if onoff == "off":
                        cow = False
                        SendIRCRaw("NOTICE %s COW OFF" % nick)
                    if onoff == "on":
                        cow = True
                        SendIRCRaw("NOTICE %s COW ON" % nick)
                if cmd == "cowpart":
                    SendIRCRaw("PART :#" + msg.split()[4])
                if cmd == "cowjoin":
                    SendIRCRaw("JOIN :#" + msg.split()[4])
                if cmd == "cowshit":
                    if nick == "Banhammer":
                        SendIRCRaw("QUIT MOO")
                        quit()
                if cmd == "status":
                    SendPM(onoff)
# Cows -----------------------------------------------------
        c = " ".join(msg.split()[3:][1:])
        cnum = int(len(c))
        cdash = cnum*"_"
        cdash2 = cnum*"-"
        def say_beginning(cdash,c,cdash2):
            SendText(" _%s_" % cdash)
            SendText("< %s >" % c)
            SendText(" -%s-" % cdash2)
        def thought_beginning(cdash,c,cdash2):
            SendText(" _%s_" % cdash)
            SendText("( %s )" % c)
            SendText(" -%s-" % cdash2)
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
            SendIRCRaw("PRIVMSG %s :\x01ACTION cooks up some fancy steak for %s.\x01" % (location, beef_for))
