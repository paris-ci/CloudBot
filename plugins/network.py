import socket
import time
import random
import subprocess
import re
import os

from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens
from cloudbot.util.colors import parse
from data.ports import toScan


def scanport(IP, PORT):
	time.sleep(0.005)
	# noinspection PyBroadException
	try:
		s = socket.socket()
		s.connect((IP, PORT))
		return True
	except:
		return False


@hook.command("portscan1", "ps1", "scan1")
def scanOne(reply, text, nick, notice):
	if getTokens(nick) < 1000:
		notice("You don't have enough tokens to do a portscan (1000 needed)... Help a little more !")
		return None

	args = text.split()

	try:
		IP = str(args[0])
		PORT = int(args[1])
	except IndexError:
		notice("Syntax : !ps1 IP PORT. Use !ps3000 for the 3000 most used ports")
		return None

	takeTokens(100, nick, notice)
	socket.setdefaulttimeout(2)
	reply("Scanning port number " + str(PORT) + " for ip " + str(IP))

	result = scanport(IP, PORT)

	if result:
		reply("The port " + str(PORT) + " of the IP " + IP + " is OPEN !")
	elif not result:
		reply("The port " + str(PORT) + " of the IP " + IP + " is CLOSED ! ")


@hook.command("portscan3000", "scan3000", "ps3000")
def scan3000(reply, text, nick, notice):
	if getTokens(nick) < 10000:
		notice("You don't have enough tokens to do a portscan3000 (10000 needed)... Help a little more !")
		return None

	if not text:
		reply("Please specify an IP address/ dns ! !ps3000 IP")

	scanned = 0

	takeTokens(500, nick, notice)
	IP = text
	openPorts = []
	socket.setdefaulttimeout(2)
	reply("Scanning 3000 ports... It's a long task, you'll have to wait !")

	for PORT in toScan:
		scanned += 1
		if scanport(IP, PORT):
			openPorts.append(PORT)

		if scanned % 250 == 0:
			notice("Progress (" + str(IP) + "): " + str(scanned) + " / 3000")

	openPorts.sort()
	reply("Open ports found for " + text + " (" + str(len(openPorts)) + "): " + str(openPorts))


@hook.command("passwordgenerator", "genpass", "passgen", "password")
def passgen(reply, nick, notice):
	if getTokens(nick) < 100:
		notice("You don't have enough tokens to do a password generation (100 needed)... Help a little more !")
		return None

	takeTokens(5, nick, notice)

	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890^=+/:.;?,-_)&"'(!<>'
	pw_length = 10
	mypw = ""

	for i in range(pw_length):
		next_index = random.randrange(len(alphabet))
		mypw += alphabet[next_index]

	reply("I just generated a 10 chars random password for you ! Here you go ! " + mypw)


unix_ping_regex = re.compile(r"(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
win_ping_regex = re.compile(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms")


@hook.command()
def ping(text, reply):
	"""<host> [count] - pings <host> [count] times"""

	args = text.split(' ')
	host = args[0]

	# check for a second argument and set the ping count
	if len(args) > 1:
		count = int(args[1])
		if count > 20:
			count = 20
	else:
		count = 5

	count = str(count)

	if os.name == "nt":
		args = ["ping", "-n", count, host]
	else:
		args = ["ping", "-c", count, host]

	reply("Attempting to ping {} {} times...".format(host, count))
	try:
		pingcmd = subprocess.check_output(args).decode("utf-8")
	except subprocess.CalledProcessError:
		return "Could not ping host."

	if re.search("(?:not find host|timed out|unknown host)", pingcmd, re.I):
		return "Could not ping host."

	if os.name == "nt":
		m = re.search(win_ping_regex, pingcmd)
		r = int(m.group(2)) - int(m.group(1))
		return "min: %sms, max: %sms, average: %sms, range: %sms, count: %s" \
			   % (m.group(1), m.group(2), m.group(3), r, count)
	else:
		m = re.search(unix_ping_regex, pingcmd)
		return "min: %sms, max: %sms, average: %sms, range: %sms, count: %s" \
			   % (m.group(1), m.group(3), m.group(2), m.group(4), count)


def pingavg(host):
	if os.name == "nt":
		args = ["ping", "-n", "2", host]
	else:
		args = ["ping", "-c", "2", host]

	try:
		pingcmd = subprocess.check_output(args).decode("utf-8")
	except subprocess.CalledProcessError:
		return -1

	if re.search("(?:not find host|timed out|unknown host)", pingcmd, re.I):
		return -1

	if os.name == "nt":
		m = re.search(win_ping_regex, pingcmd)
		return m.group(3)
	else:
		m = re.search(unix_ping_regex, pingcmd)
		return m.group(2)


@hook.command("harmonystatus", "hhstatus", "harmony", "ddos", "pinghh", "hh")
def hhstatus(reply, notice, nick):
	if getTokens(nick) < 100:
		notice("You don't have enough tokens. (100 needed)... Help a little more !")
		return None

	notice("Je vérifie le statut des serveurs ! Cela prends environ 20 secondes, voire moins !")
	InternalHosts = sorted(["lisa", "homer", "marge", "maggie", "flanders", "www", "apu", "burns", "irc"])
	ExternalHosts = sorted(["bukkit.fr", "google.fr", "ovh.com", "proof.ovh.net"])
	#	dead = []
	#	good = []
	#	bad = []
	toreply = "NODES : "

	for host in InternalHosts:
		avg = float(pingavg(host + ".harmony-hosting.com"))

		if avg == -1:
			# dead.append(host)
			toreply += "$(dark_red)" + host + "(ERR)" + "$(clear) "
		elif avg <= 20:
			# good.append(host)
			toreply += "$(dark_green)" + host + "$(clear) "
		elif avg <= 1000:
			# bad.append(host)
			toreply += "$(orange)" + host + "(" + str(avg) + " ms)" + "$(clear) "
		else:
			# dead.append(host)
			toreply += "$(red)" + host + "(" + str(avg) + " ms)" + "$(clear) "

	toreplyINT = parse(toreply)

	toreply = "SERVICES: "
	for host in ExternalHosts:
		avg = float(pingavg(host))

		host = host.replace('.', '_')

		if avg == -1:
			# dead.append(host)
			toreply += "$(dark_red)" + host + "$(clear) "
		elif avg <= 20:
			# good.append(host)
			toreply += "$(dark_green)" + host + "$(clear) "
		elif avg <= 1000:
			# bad.append(host)
			toreply += "$(orange)" + host + "(" + str(avg) + " ms)" + "$(clear) "
		else:
			# dead.append(host)
			toreply += "$(red)" + host + "$(clear) "

	toreplyEXT = parse(toreply)

	reply(toreplyINT)
	reply(toreplyEXT)


@hook.command("serverinfo", "servinfo")
def servinfo(reply, text):
	host = text

	# First of all, check the ping !
	ping = pingavg(host)

	# Check if ssh is working (port 22 open)
	sshWorking = scanport(host, 22)

	# Check if web HTTP is working
	httpWorking = scanport(host, 80)

	# Check if web HTTP is working
	httpsWorking = scanport(host, 443)

	# Check if DNS is working
	dnsWorking = scanport(host, 53)

	# Check if SMTP is working
	smtpWorking = scanport(host, 25)

	# Lets reply that !
	toreply = ""

	if ping == -1:
		toreply += "$(dark_red)ping $(clear)"
	elif ping <= 20:
		toreply += "$(dark_green)ping $(clear)"
	elif ping <= 1000:
		toreply += "$(orange)ping (" + str(ping) + " ms)" + "$(clear)"
	else:
		toreply += "$(red)ping $(clear)"

	if sshWorking:
		toreply += "$(dark_green)ssh $(clear)"
	else:
		toreply += "$(red)ssh $(clear)"

	if httpWorking:
		toreply += "$(dark_green)http $(clear)"
	else:
		toreply += "$(red)http $(clear)"

	if httpsWorking:
		toreply += "$(dark_green)https $(clear)"
	else:
		toreply += "$(red)https $(clear)"

	if dnsWorking:
		toreply += "$(dark_green)dns $(clear)"
	else:
		toreply += "$(red)dns $(clear)"

	if smtpWorking:
		toreply += "$(dark_green)smtp  $(clear)"
	else:
		toreply += "$(red)smtp $(clear)"
