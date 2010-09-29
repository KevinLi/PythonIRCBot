#! usr/bin/env python
"""
Program: CowBot
Version: 0.0.2
Author: banhammer
Editors: Cam

Description: CowBot is a bot designed to send different ascii cows and text to an IRC channel
"""

import socket
import sys

irc = socket.socket()
network = 'irc.n0v4.com'
port = 6667
ircchannel = '#lobby'

ircname = 'Cow' # max 30 characters
realname = "lolcow"
ident = "MOO"

crlf = "\r\n"
onoff = "off"
cow = False

admins = ["Banhammer","Horkx3"]

def SendIRCRaw(x):
    irc.send(x+crlf)
    
def SendText(text):
    irc.send("PRIVMSG %s :%s" % (location, text) + crlf)

def SendPM(text):
    irc.send("PRIVMSG %s :%s" % (nick, text) + crlf)

irc.connect((network, port))
SendIRCRaw("NICK %s" % ircname)
SendIRCRaw("USER %s **** **** :%s" % (ident, realname))
#sleep(3)
#SendIRCRaw("MSG NickServ IDENTIFY password")

# [0]host, [1]channel, [2]nick, [3+]message
while True:
# Parse Message --------------------------------------------    
        msg = irc.recv(512)
        print msg
        if len(msg.split())>0:
            if msg.split()[0] == "PING":
                SendIRCRaw("PONG %s" % msg.split()[1])
        if len(msg.split())>1:
            if msg.split()[1] == "001":
                print "001"
                SendIRCRaw("JOIN %s" % ircchannel)
        if len(msg.split())>=4:
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
        #if location == ircname:
        #    SendPM("Message ignored.")
# Admin Commands -------------------------------------------
        cowc = " ".join(msg.split()[3:][1:])
        cowcnum = int(len(cowc))
        cowdash = cowcnum*"-"
        def cow_beginning(cowdash,cowc):
            SendText(" -%s-" % cowdash)
            SendText("< %s >" % cowc)
            SendText(" -%s-" % cowdash)
        if nick in admins:
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
                SendIRCRaw("QUIT")
                quit()
            if cmd == "status":
                SendPM(onoff)
# Cows -----------------------------------------------------
        if cow is True:
            if cmd == "cowsay":
                cow_beginning(cowdash,cowc)
                SendText("        \   ^__^")
                SendText("         \  (oo)\_______")
                SendText("            (__)\       )\/\ ")
                SendText("                ||----w |")
                SendText("                ||     ||")
            if cmd == "cowdrunk":
                cow_beginning(cowdash,cowc)
                SendText("        \   ^__^")
                SendText("         \  (**)\_______")
                SendText("            (__)\       )\/\ ")
                SendText("             U  ||----w |")
                SendText("                ||     ||")
            if cmd == "cowsex":
                cow_beginning(cowdash,cowc)
                SendText("      \                _")
                SendText("       \              (_)")
                SendText("        \   ^__^       / \ ")
                SendText("         \  (oo)\_____/_\ \ ")
                SendText("            (__)\       ) /")
                SendText("                ||----w ((")
                SendText("                ||     ||>> ")
# Cow Off Notification -------------------------------------
        elif cmd == "cowsay":
            SendText("Cow is off.")
        elif cmd == "cowdrunk":
            SendText("Cow is off.")
        elif cmd == "cowsex":
            SendText("Cow is off.")
# Public Commands ------------------------------------------
        if cmd == "cowhelp":
            SendPM("Available commands are:")
            SendPM("cowhelp          status")
            SendPM("cow on/off      cowshit")
            SendPM("cowjoin         cowpart")
            SendPM("-----------------------")
            SendPM("cowsay         cowdrunk")
            SendPM("cowsex")
        if cmd == ";_;":
            SendText("Moo.")
