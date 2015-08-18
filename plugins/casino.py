"""
casino.py

A little fun game

Created By:
    - paris-ci <http://api-d.com/>

License:
    GNU General Public License (Version 3)"""
from math import ceil
import json
from random import randrange
import random

from cloudbot import hook

default = {"money": 100, "bet": 1, "cards": ""}

# save / load

def saveToDisk(data):
	with open('data/casino.json', 'w') as outfile:
		json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def loadFromDisk():
	file = open('data/casino.json')
	data = json.load(file)
	return data


# Parsing

def getMoney(nick):
	data = loadFromDisk()  # Get data from file
	argent = int(data.get(nick, default)["money"])  # Extract money of a player
	return argent


def getBet(nick):
	data = loadFromDisk()  # Get data from file
	bet = int(data.get(nick, default)["bet"])  # Extract bet of a player
	return bet


def getCards(nick):
	data = loadFromDisk()  # Get data from file
	cards = data.get(nick, default)["cards"]  # Extract cards of a player
	return list(cards)


def savePlayerData(nick, argent=None, mise=None, cards=None):
	if not argent:
		argent = getMoney(nick)

	if not mise:

		mise = getBet(nick)

	if not cards:

		cards = getCards(nick)

	data = loadFromDisk()
	data[nick] = {"money": int(argent), "bet": int(mise), "cards": list(cards)}  # Save to data
	saveToDisk(data)  # Save to disk


# Money

@hook.command("setMoney", permissions=["botcontrol"])
def setMoney(reply, text):
	args = text.split()
	nick = args[0]
	argent = args[1]

	oldArgent = getMoney(nick)  # Extract money of a player

	savePlayerData(nick, argent=money)

	reply(nick + " had " + str(oldArgent) + "$. He/She have " + str(argent) + "$ now!")


@hook.command("money", "bal", "balance")
def money(nick, notice, text):
	try:
		player = text.split()[0]
		notice(player + " have " + str(getMoney(player)) + "$ !")
		return None

	except IndexError:
		notice("You have " + str(getMoney(nick)) + "$ !")
		return None


def checkMoneyBet(nick, notice):
	argent = getMoney(nick)
	mise = getBet(nick)
	if argent < 50:
		notice("Hey, you're lucky, you found money in the back of the casino.")
		notice("You now have 150$")
		argent = 150
		savePlayerData(nick, argent=argent)

	if mise > argent:
		notice("You try to bet too much ! You have only " + str(argent) + ". Change bet with !bet")
		return None

	if mise == 1:
		notice("You can change your bet with !bet")

	return argent, mise


########
# Wheel
########

def runEngine(argent, mise, reply, notice):
	notice("Welcome to the casino ! You have " + str(argent) + "$ !")
	numero_gagnant = randrange(50)
	nombre_mise = randrange(50)
	notice("You bet on >> " + str(nombre_mise) + " <<")

	if numero_gagnant == nombre_mise:
		print("Congrats, the exact same number ! You won" + str(mise * 3) + "$ !")

		argent += mise * 3

	elif numero_gagnant % 2 == nombre_mise % 2:  # ils sont de la même couleur

		mise = ceil(mise * 0.5)

		reply("Same color ! (The wheel was on " + str(numero_gagnant) + " ). You won : " + str(mise) + "$")

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

	notice("You now have " + str(getMoney(nick)) + "$ !")


@hook.command("bet")
def setBet(nick, notice, text):
	argent = getMoney(nick)  # Extract money of a player
	mise = int(text)  # Save the bet

	if mise > argent:
		notice("You try to bet too much ! You have only " + str(argent) + ".")
		return None

	if mise < 1:
		notice("Negative bet or < 1. Try a positive one ;)")
		return None

	savePlayerData(nick, mise=mise)

	notice("Done. Your bet is now : " + str(mise) + "$")


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
		result = BlackJack.cards[0]
		BlackJack.cards.remove(BlackJack.cards[0])
		return result

	# end draw and remove a card

	def reset(self):
		self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
					  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
		random.shuffle(BlackJack.cards)

	# end reset deck and shuffle


def startBJ(notice, nick):
	if not getCards(nick):
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


def getBJ(notice, nick):
	game = BlackJack()
	cards = getCards(nick)

	PT = int(cards[0])

	if PT > 21:
		endBJ(notice, nick)
		return None

	PX = int(game.draw())
	notice("You drew a " + str(PX))
	PT += PX
	notice("Your total is: " + str(PT))
	savePlayerData(nick, cards=[PT, cards[1]])


def endBJ(notice, nick):
	game = BlackJack()

	cards = getCards(nick)
	PT = int(cards[0])
	D1 = int(cards[1])
	if PT > 21:
		notice("Bust!")
	elif PT == 21:
		notice("Yay! 21!")
	else:
		notice("Your hand was " + str(PT))
	# end player hand

	D2 = game.draw()  # dealer card 2
	notice("Dealer has: " + str(D1) + " and " + str(D2))
	DT = D1 + D2
	notice("Dealer's total is: " + str(DT))

	while DT < 17:
		DX = game.draw()
		notice("Dealer drew a " + str(DX))
		DT = DX + DT
		notice("Dealer's hand is: " + str(DT))
	# end while the dealer's hand is < 17

	if DT == 21:
		notice("Dealer got 21!")
		notice("You got " + str(PT))
	elif DT < 21:
		notice("Dealer got" + str(DT))
		notice("You got " + str(PT))
	else:
		notice("Dealer busts")
		notice("You got " + str(PT))

	savePlayerData(nick, cards=[])


@hook.command("bj", "blackjack")
def blackJack(notice, text, nick):
	if text == "start":
		startBJ(notice, nick)

	elif text == "get":
		getBJ(notice, nick)

	if text == "end":
		endBJ(notice, nick)
