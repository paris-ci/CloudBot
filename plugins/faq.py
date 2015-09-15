import json

from cloudbot import hook
from cloudbot.util import web

def loadfromdisk():
	file = open('data/faq.json', 'r')
	data = json.load(file)
	return data


def saveToDisk(data):
	with open('data/faq.json', 'w') as outfile:
		json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


@hook.command("faq")
def faq(text, reply, notice):
	data = loadfromdisk()
	text = text.split()

	try:
		reponse = data[text[0]]

	except:
		reply("Le mot recherché n'as pas été trouvé dans la FAQ !")
		return

	try:
		notice(reponse, text[1])
		notice("Transmis !")

	except:
		reply(reponse)


@hook.command("faqadd", "addfaq", permissions=["faq"])
def faqadd(text, reply):

	data = loadfromdisk()
	text = text.split()

	word = text[0]
	answer = ' '.join(text[1:])

	data[word] = answer

	saveToDisk(data)

	reply("Le mot " + word + " as été ajouté a la FAQ. Il refere à : " + answer)

@hook.command("faqlist","listfaq")
def listfaq(reply):
	file = open('data/faq.json', 'r').read()
	lien = web.paste(file)
	reply(str(lien))