#! usr/bin/env python
"""
Program: General purpose IRC bot
Version: 1.0.4.78
Author: Kevin
Site: https://github.com/kevinli
Description:
"""
# Imports ---------------
import socket
import random
import time
import urllib
# Bot details -----------
selfnick = ident = 'HerpDerp' # max 30 characters
realname = 'Hurr Durr'
# Constants -------------
irc = socket.socket()
port = 6667
# Variables -------------
lolcount = 0
annoyed = 0
lol = [True]
cow = wat = True
nopuddi = False
noucounter = 0
noutoggle = 1
timer = pudditime = time.time()
pudditimerand = random.randint(3600,7200)
nourand = random.randint(1,4) #random number, limit of "no u"'s
# Userlist ----
admins = []
allowedhosts = []
toignore = []
# IRC functions ---------
def SendIRCRaw(rawtext):
    irc.send(rawtext+'\r\n')
def SendText(text):
    irc.send("PRIVMSG {0} :{1}".format(location, text) + '\r\n')
def SendPM(text):
    irc.send("PRIVMSG {0} :{1}".format(nick, text) + '\r\n')
# Misc bot functions
def cowsay(cdash,text,cdash2):
    SendText(" _{0}_".format(cdash))
    SendText("< {0} >".format(text))
    SendText(" -{0}-".format(cdash2))
    SendText("        \   ^__^")
    SendText("         \  (oo)\_______")
    SendText("            (__)\       )\\/\\")
    SendText("                ||----w |")
    SendText("                ||     ||")
def memes(numberofmemes):
    memeurl = "http://api.automeme.net/text?lines={0}".format(numberofmemes)
    memes = urllib.urlopen(memeurl).readlines()
    print(memes)
    for i in range(0,len(memes)):
        SendIRCRaw("PRIVMSG {0} {1}".format(location, memes[i]))
def puddi():
    pudditext = "PUDDI"*random.randint(10,60)
    SendText(pudditext)
# Start: Settings
network = raw_input("Server       (default: ): ")
if network == "":
    network = ""
password = raw_input("Password              (default: none): ")
IRCChannel0 = "#" + raw_input("Channel 0           (default: #lobby): #")
if IRCChannel0 == "#":
    IRCChannel0 = "#lobby"
JoinChannel1 = raw_input("Join second channel? Y/N (default: N): ").lower()
if JoinChannel1 == "y":
    IRCChannel1 = "#" + raw_input("Channel 1           (enter to cancel): #")
raw_input("Press enter to connect...")
log = open('PyIRCBotLog.txt','a')
# Start: Connection
print("\nConnecting...")
irc.connect((network, port))
SendIRCRaw("USER {0} **** **** :{1}".format(ident, realname))
SendIRCRaw("NICK :{0}".format(selfnick))
time.sleep(1)
if password == '': pass
else: SendIRCRaw("NickServ IDENTIFY {0}".format(password))
SendIRCRaw("MODE {0} +B".format(selfnick))
print("Connected.")
# [0]host, [1]channel, [2]nick, [3:]message
if JoinChannel1 == 'y' and IRCChannel1 != '#':
    SendIRCRaw("JOIN :{0}".format(IRCChannel1))
while True:
# Parse Message
    try:
        msg = irc.recv(512)
        log.write(msg)
        msgsplit = msg.split()
        print(msg)
    except: pass
    try:
        if msg.split()[0] == "PING":
            SendIRCRaw("PONG :{0}".format(network))
    except:
        print("Could not respond to server ping.")
        break
    if len(msg.split()) > 1 and msg.split()[1] == "372":
        SendIRCRaw("JOIN :{0}".format(IRCChannel0))
    if len(msg.split()) > 3 and msg.split()[1] == "KICK":
        SendIRCRaw('JOIN :{0}'.format(msg.split()[2]))
    if len(msg.split()) >= 4:
        try: host = msgsplit[0].split("@")[1]
        except: host = ""
        text = " ".join(msg.split()[3:][1:])
        cmd = msg.split()[3][1:].lower()
        location = msg.split()[2]
        nick = msg.split("!")[0][1:]
    else:
        cmd = location = nick = text = ""
# Admin Commands
    if nick in admins and host in allowedhosts:
        if msg.split()[1] == "INVITE":
            SendIRCRaw("JOIN :{0}".format(cmd))
        if cmd == "[part]":
            try: SendIRCRaw("PART :#{0}".format(msg.split()[4]))
            except: pass
        if cmd == "[join]":
            try: SendIRCRaw("JOIN :#{0}".format(msg.split()[4]))
            except: pass
        if cmd == "[herpderp]":
            SendIRCRaw("QUIT HERP DERP")
            log.close()
            quit()
        if cmd == "[sendraw]":
            SendIRCRaw(" ".join(msg.split()[3:][1:]))
        if cmd == "[cycle]":
            SendIRCRaw("PART :{0}".format(location))
            SendIRCRaw("JOIN :{0}".format(location))
        if cmd == "lolcount":
            SendText(lolcount)
        if cmd == 'resetlol':
            lolcount = 0
            print('lolcount: '+str(lolcount))
# Public Commands
    if cmd == "wat":
        if text == "" and nick not in toignore and wat != False:
            SendText("wat")
        elif text == "off":
            wat == False
        elif text == "on":
            wat == True
#    if ":laugh" in msgsplit or "laugh" in msgsplit or cmd == "laugh":
#        try:
#            lolindex = msgsplit.index(":laugh")
#            lo = int(" ".join(msg.split()[3:][lolindex:]))
#            if lo >= 0 and lo < 100:
#                lol = "LO"*lo
#                SendText(lol+"L")
#            elif lo > 100:
#                SendText("LO"*100)
#        except: pass
    if cmd == "<3":
        if 1 == random.randint(0, 3):
            SendText("<3!")
        elif 6 <= random.randint(0,9):
            SendText("<3")
        else: pass
    if cmd == "no" and text.lower() == 'u' and \
    nick not in toignore and noutoggle == 1:
        if noucounter < nourand:
            SendText("NO U")
            noucounter += 1 #counter, counts number of no u's sent
        elif noucounter == nourand:
            SendText("FINE, ME")
            noucounter += 1
            noutoggle = 0
    if cmd == "meme" and text == "":
        meme = urllib.urlopen("http://api.automeme.net/text?lines=1").read()
        SendIRCRaw("PRIVMSG {0} {1}".format(location, meme))
    if cmd == "memes":
        try:
            numbermemes = int(msg.split()[4])
            print(numbermemes)
            if numbermemes <= 4:
                memes(numbermemes)
            elif nick in admins and numbermemes > 25:
                memes(20)
        except: pass
		# MEMES, MEMES EVERYWHERE
    if cmd == "puddi" and nopuddi == False:
        puddi()
        nopuddi = True
        # STICK THIS SHIT IN THE TIMED RESET, WITH A LIMIT. two lines down.
# Timed Reset
    if time.time() > timer+600: # 600 seconds = 10 minutes
        timer = time.time() #Reset timer
        noutoggle = 1
        noucounter = wat = 0
        nourand = random.randint(1,3)
        nopuddi = False
        print('Reset')
# BEING ANNOYING
    if cmd == 'wat' or cmd == 'ok' and nick in toignore:
        annoyed += 1
        print('annoyed:'+annoyed)
        if annoyed == 20:
			SendText('SHUT THE FUCK UP, {0}'.format(nick))
			annoyed = 0
# Random events
#    if time.time() > pudditime+pudditimerand:
#        puddi()
#        pudditime = time.time()
#        pudditimerand = random.randint(3600,7200)
# Cowsay!
    if cmd == "cowsay" and cow is True and text != "":
        cowsay(len(text)*"_",text,len(text)*"-")
# lol counter
    for i in msgsplit:
        i = i.lower()
        if 'lol' in i and i != ':resetlol':
            lolcount += 1
            print('lolcount:'+str(lolcount)+'\n')
    if lolcount % 10 == 0 and lolcount != 0 and lol[lolcount/10-1] == True:
        SendText("{0} lols have been lol'd.".format(lolcount))
        lol[lolcount/10-1] = False
        lol.append(True)
        print(lol)
