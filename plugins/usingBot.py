""" Tokens system for the network commands

it expects a valid empty folder in data/usedata

"""

import json

from cloudbot import hook

default = """{
"tokens": 0
}"""


def saveToDisk(data, nick):
	with open('data/usedata/' + nick + '.json', 'w') as outfile:
		json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def loadFromDisk(nick):
	try:
		file = open('data/usedata/' + nick + '.json', 'r')
		data = json.load(file)
		return data
	except IOError:
		file = open('data/usedata/' + nick + '.json', 'w')
		file.write(str(default))
		file.close()
		file = open('data/usedata/' + nick + '.json', 'r')
		data = json.load(file)
		return data


def getTokens(nick):
	data = loadFromDisk(nick)  # Get data from file
	argent = int(data.get("tokens", default))  # Extract tokens of a player
	return argent


def giveTokens(NumberOftokens, nick):
	argent = getTokens(nick)
	argent += NumberOftokens
	savePlayerData(nick=nick, argent=argent)


def takeTokens(NumberOftokens, nick, notice=None):
	argent = getTokens(nick)
	argent = argent - NumberOftokens
	if notice is not None:
		notice("-" + str(NumberOftokens) + " Left: " + str(argent))
	savePlayerData(nick=nick, argent=argent)


def savePlayerData(nick, argent=None):
	if not argent:

		argent = getTokens(nick)

	data = {"tokens": int(argent)}  # Save to data
	saveToDisk(data, nick)  # Save to disk


@hook.command("Treset", "TresetPlayer", permissions=["botcontrol"])
def reset(nick, reply, text):
	saveToDisk(default, nick)  # Save to disk
	reply(text + " usetokens was deleted by " + nick)


@hook.command("setTokens", permissions=["botcontrol"])
def setTokens(reply, text):
	args = text.split()
	try:
		nick = args[0]
		argent = args[1]
	except IndexError:
		reply("Syntax error : !setTokens nickname number")
		return None

	oldArgent = getTokens(nick)  # Extract tokens of a player

	savePlayerData(nick, argent=argent)

	reply(nick + " had " + str(oldArgent) + " tokens. He/She have " + str(argent) + " tokens now!")


@hook.command("tokens")
def tokens(nick, notice, text):
	try:
		player = text.split()[0]
		notice(player + " have " + str(getTokens(player)) + " tokens !")
		return None

	except IndexError:
		notice("You have " + str(getTokens(nick)) + " tokens !")
		return None


@hook.regex("(.*)")
def addTokensPriv(nick):
	giveTokens(10, nick)
