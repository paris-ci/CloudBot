""" Tokens system for the network commands

it expects a valid empty folder in data/usedata

"""

from cloudbot import hook
from cloudbot.util import WorkingWithFiles
default = """{
"tokens": 0
}"""

WorkingWithFiles.checkExistsPath("data/usedata/")



def getTokens(nick):
	data = WorkingWithFiles.JSONloadFromDisk('data/usedata/' + nick + '.json', default)  # Get data from file
	tokens = int(data.get("tokens", default))  # Extract tokens of a player
	return tokens


def giveTokens(NumberOftokens, nick):
	tokens = getTokens(nick)
	tokens += NumberOftokens
	saveUseData(nick=nick, tokens=tokens)


def takeTokens(NumberOftokens, nick, notice=None):
	tokens = getTokens(nick)
	tokens = tokens - NumberOftokens
	if notice is not None:
		notice("-" + str(NumberOftokens) + " Left: " + str(tokens))
	saveUseData(nick=nick, tokens=tokens)


def saveUseData(nick, tokens):
	data = {"tokens": int(tokens)}  # Save to data
	WorkingWithFiles.JSONsaveToDisk(data, 'data/usedata/' + nick + '.json')  # Save to disk


@hook.command("Treset", "TresetPlayer", permissions=["botcontrol"])
def reset(nick, reply, text):
	WorkingWithFiles.JSONsaveToDisk(default, 'data/usedata/' + nick + '.json')  # Save to disk
	reply(text + " usetokens was deleted by " + nick)


@hook.command("setTokens", permissions=["botcontrol"])
def setTokens(reply, text):
	args = text.split()
	try:
		nick = args[0]
		tokens = args[1]
	except IndexError:
		reply("Syntax error : !setTokens nickname number")
		return None

	oldTokens = getTokens(nick)  # Extract tokens of a player

	saveUseData(nick, tokens)

	reply(nick + " had " + str(oldTokens) + " tokens. He/She have " + str(tokens) + " tokens now!")


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
