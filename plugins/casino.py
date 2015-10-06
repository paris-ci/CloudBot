"""
casino.py

A little fun game

it expects a valid empty json file in data/casino.json (contents : {})

Created By:
    - paris-ci <http://api-d.com/>

License:
    GNU General Public License (Version 3)"""
from random import randrange
import random
import time

from math import ceil
from cloudbot import hook
from cloudbot.util import WorkingWithFiles

default = {"money": 100, "bet": 1, "cards": ""}

# save / load

WorkingWithFiles.checkExistsFile("data/casino.json")


# Parsing

def getMoney(nick):
	data = WorkingWithFiles.JSONloadFromDisk('data/casino.json', default)  # Get data from file
	argent = int(data["nick"]["money"])  # Extract money of a player
	return argent


def getBet(nick):
	data = WorkingWithFiles.JSONloadFromDisk('data/casino.json', default)  # Get data from file
	bet = int(data.get["nick"]["bet"])  # Extract bet of a player
	return bet


def getCards(nick):
	data = WorkingWithFiles.JSONloadFromDisk('data/casino.json', default)  # Get data from file
	cards = data.get["nick"]["cards"]  # Extract cards of a player
	return list(cards)


def savePlayerData(nick, argent="NotProvided", mise=None, cards=None):
	if argent == "NotProvided":

		argent = getMoney(nick)

	if not mise:

		mise = getBet(nick)

	if not cards:

		cards = getCards(nick)

	data = WorkingWithFiles.JSONloadFromDisk('data/casino.json', default)
	data[nick] = {"money": int(argent), "bet": int(mise), "cards": list(cards)}  # Save to data
	WorkingWithFiles.JSONsaveToDisk(data, 'data/casino.json')  # Save to disk


@hook.command("reset", "resetPlayer", permissions=["botcontrol"])
def reset(nick, reply, text):
	data = WorkingWithFiles.JSONloadFromDisk('data/casino.json', default)
	data[text] = default  # Save to data
	WorkingWithFiles.JSONsaveToDisk(data, 'data/casino.json')  # Save to disk
	reply(text + " stats was deleted by " + nick)


# Money

@hook.command("setMoney", permissions=["botcontrol"])
def setMoney(reply, text):
	args = text.split()
	try:
		nick = args[0]
		argent = args[1]
	except IndexError:
		reply("Syntax error : !setMoney nickname number")
		return None

	oldArgent = getMoney(nick)  # Extract money of a player

	savePlayerData(nick, argent=argent)

	reply(nick + " had $" + str(oldArgent) + ". He/She have $" + str(argent) + " now!")


@hook.command("money", "bal", "balance")
def money(nick, notice, text):
	try:
		player = text.split()[0]
		notice(player + " have $" + str(getMoney(player)) + " !")
		return None

	except IndexError:
		notice("You have $" + str(getMoney(nick)) + " !")
		return None


def checkMoneyBet(nick, notice):
	argent = getMoney(nick)
	mise = getBet(nick)
	if argent < 50:
		notice("Hey, you're lucky, you found money in the back of the casino.")
		notice("You now have $150")
		argent = str(150)
		savePlayerData(nick, argent=argent)

	if mise > argent:
		notice("You try to bet too much ! You have only $" + str(argent) + ". Change bet with !bet")
		return None

	if mise == 1:
		notice("You can change your bet with !bet")

	return argent, mise


########
# Wheel
########

def runEngine(argent, mise, reply, notice):
	notice("Welcome to the casino ! You have $" + str(argent) + " !")
	numero_gagnant = randrange(50)
	nombre_mise = randrange(50)
	notice("You bet on >> " + str(nombre_mise) + " <<")

	if numero_gagnant == nombre_mise:
		reply("Congrats, the exact same number ! You won $" + str(mise * 3) + " !")

		argent += mise * 3

	elif numero_gagnant % 2 == nombre_mise % 2:  # ils sont de la même couleur

		mise = ceil(mise * 0.5)

		reply("Same color ! (The wheel was on " + str(numero_gagnant) + " ). You won : $" + str(mise))

		argent += mise

	else:

		reply("Sorry, not this time, you loose ! Too bad !")

		argent = argent - mise

	return argent


@hook.command("roulette", "wheel")
def launchGame(nick, reply, notice):
	argent, mise = checkMoneyBet(nick, notice)

	argent = runEngine(argent, mise, reply, notice)  # Return money of a player

	savePlayerData(nick, argent=argent)

	notice("You now have $" + str(getMoney(nick)) + " !")


@hook.command("bet")
def setBet(nick, notice, text):
	argent = getMoney(nick)  # Extract money of a player
	mise = int(text)  # Save the bet

	if mise > argent:
		notice("You try to bet too much ! You have only $" + str(argent) + ".")
		return None

	if mise < 1:
		notice("Negative bet or < 1. Try a positive one ;)")
		return None

	savePlayerData(nick, mise=mise)

	notice("Done. Your bet is now : $" + str(mise))


#######
# Black Jack
#######

class BlackJack:
	cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
			 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
			 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
			 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

	@staticmethod
	def draw():
		return randrange(1, 10)

	# end draw and remove a card

	def reset(self):
		self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
		random.shuffle(BlackJack.cards)

	# end reset deck and shuffle


def startBJ(notice, nick):
	if not getCards(nick) or getCards(nick)[0] == "end":
		notice("You started a new BlackJack game with the dealer")
		game = BlackJack()
		game.reset()
		D1 = game.draw()  # dealer card 1
		P1 = game.draw()  # player card 1
		P2 = game.draw()  # player card 2
		notice("Cards drawn were " + str(P1) + " and " + str(P2))
		PT = P1 + P2
		cards = [PT, D1]
		savePlayerData(nick, cards=cards)
		print(list(cards))

	else:
		cards = getCards(nick)

	notice("Your total is: " + str(cards[0]))
	notice("Dealer has: " + str(cards[1]) + " and a hidden card")
	notice("End getting cards with !bj end, get another with !bj get")


def getBJ(notice, nick, reply):
	game = BlackJack()
	cards = getCards(nick)

	try:
		PT = int(cards[0])
	except ValueError:
		notice("Start the game with !bj start")
		return None

	if PT > 21:
		endBJ(notice, nick, reply)
		return None

	PX = int(game.draw())
	notice("You drew a " + str(PX))
	PT += PX
	notice("Your total is: " + str(PT))
	savePlayerData(nick, cards=[PT, cards[1]])


def endBJ(notice, nick, reply):
	game = BlackJack()
	argent, mise = checkMoneyBet(nick, notice)

	cards = getCards(nick)
	try:
		PT = int(cards[0])
	except ValueError:
		notice("Start the game with !bj start")
		return None
	D1 = int(cards[1])
	if PT > 21:
		notice("Oh NOOO ! You busted!")
		notice("You got " + str(PT))
		argent = argent - mise
		reply("You've lost " + str(mise) + "$ ! You now have " + str(argent) + "$ ")
		savePlayerData(nick, argent=argent, cards=["end"])
		return None

	elif PT == 21:
		notice("Yay! You've got 21!")
	else:
		notice("Your hand was " + str(PT))
	# end player hand

	D2 = game.draw()  # dealer card 2
	notice("Dealer has: " + str(D1) + " and " + str(D2))
	DT = D1 + D2
	notice("Dealer's total is: " + str(DT))

	while DT < 17:
		DX = game.draw()
		time.sleep(randrange(0, 5))
		notice("Dealer drew a " + str(DX))
		DT = DX + DT

	if DT == 21:
		notice("Dealer got 21!")
	elif DT < 21:
		notice("Dealer got " + str(DT))
	else:
		notice("Dealer busts")
		argent += mise * 3
		reply("You won " + str(mise * 3) + "$ ! You now have $ " + str(argent))
		savePlayerData(nick, argent=argent, cards=["end"])
		return None

	if PT > DT:
		argent += 1.5 * mise
		reply("You won $" + str(mise * 1.5) + "! You now have $" + str(argent))


	elif PT == DT:
		argent += mise
		reply("You won $" + str(mise) + "! You now have $" + str(argent))


	else:

		argent = argent - mise
		reply("You've lost $" + str(mise) + "! You now have $" + str(argent))

	savePlayerData(nick, argent=argent, cards=["end"])
	game.reset()
	return None


@hook.command("bj", "blackjack")
def blackJack(notice, text, nick, reply):
	if text == "start":
		startBJ(notice, nick)

	elif text == "get":
		getBJ(notice, nick, reply)

	elif text == "end":
		endBJ(notice, nick, reply)

	else:
		notice("!bj start|get|end ")
