import codecs
import json
import os
import random
import asyncio
import re

from cloudbot import hook
from cloudbot.util import textgen

nick_re = re.compile("^[A-Za-z0-9_|.\-\]\[\{\}]*$", re.I)

cakes = ['au chocolat', 'à la glace', 'de l\'ange', 'à la crème', 'd\'anniversaire', 'à la carotte', 'au café', 'du diable', 'aux fruits',
		 'en pain d\'épice', 'au fromage', 'basque', 'de lunne', 'de ménage', 'marbré au chocolat', 'aux pépites de chocolat', 'moelleux']

cookies = ['aux pépites de chocolat noir', 'aux pépites de chocolat blanc', 'aux pépites de chocolat au lait', 'au sucre', 'aux raisons secs',
           'aux noix de Macadamia', 'au caramel', 'à la confiture', 'au beurre de cacahuètes', 'à la citrouille', 'aux trois chocolats', 'aux Oreos']

# <Luke> Hey guys, any good ideas for plugins?
# <User> I don't know, something that lists every potato known to man?
# <Luke> BRILLIANT

# <Akwaryoum> Hey et si je me tapais la trad de toute cette merde ?
# <Akwaryoum> SUPER IDEE
potatoes = ['Accord', 'Adirondack Blue', 'Adora', 'Adriana', 'Agata', 'Agria', 'Alaska', 'Albane', 'Alcmaria', 'Alexia', 'Allians', 'Alowa',
 		'Altesse', 'Amandine', 'Amazone', 'Amelie', 'Amflora', 'Aminca', 'Amora', 'Amyla', 'Anais', 'Aniel', 'Annabelle', 'Anoe', 'Appell',
 		'Apolline', 'Ariane', 'Arielle', 'Armada', 'Asterix', 'Atlas', 'Aubele', 'Aurea', 'Barima', 'Béa', 'Belle de Fontenay', 'Bellona',
 		'Bernadette', 'BF 15', 'Bintje', 'Bleue d\'Auvergne', 'Blondine', 'Blue Congo', 'Bonnotte de Noirmoutier', 'Cabaret', 'Caesar',
 		'Cara', 'Casablanca', 'Chacasina', 'Challenger', 'Charlène', 'Charlotte', 'Celtiane', 'Chérie', 'Columbo', 'Cooperation-88',
 		'Corne de Bamberg', 'Crisp4All', 'Cultra', 'Désirée', 'Diamant', 'Early Rose', 'Estima', 'Europa', 'Fambo', 'Felsina', 'Reine des sables',
 		'Fontane', 'Fortuna', 'Franceline', 'Garnet Chili', 'Gloria', 'Gourmandine', 'Hankkijan Tanu', 'Hankkijan Timo', 'Harmony', 'Hermes',
 		'Idole', 'Innovator', 'Institut de Beauvais', 'Kaptah Vandel', 'Kardal', 'Katahdin', 'Kennebec', 'Œil de Perdrix', 'Kufri Bahar', 'Kulta',
 		'Lady Claire', 'Lady Felicia', 'Lady Cristl', 'Lady Rosetta', 'Lenape', 'Linda', 'Lumper', 'Magnum Bonum', 'Mandola', 'Marabel', 'Marfona',
 		'Maris Bard', 'Maris Peer', 'Maris Piper', 'Markies', 'Matilda', 'Melody', 'Monalisa', 'Morene', 'Mozart', 'Nadine', 'Nectar', 'Nevsky',
 		'NewLeaf', 'NewLeaf Plus', 'Nicola', 'Olympia', 'Opperdoezer Ronde', 'Ostara', 'Osprey', 'Ozette', 'Pastusa suprema', 'Pentland Dell',
 		'Pink Fir Apple', 'Pito', 'Pompadour', 'Posmo', 'Premiere', 'Producent', 'Puikula', 'Quarantina bianca genovese', 'Quarta', 'Ramos',
 		'Ratte', 'Red Pontiac', 'Redstar', 'Record', 'Rikea', 'Rocket', 'Romano', 'Rooster', 'Rosa', 'Rosamunda', 'Roseval', 'Royal',
 		'Russet Burbank', 'Sabina', 'Sagitta', 'Saphire', 'Sarpo Mira', 'Sassy', 'Satu', 'Saturna', 'Saxon', 'Schwarzblaue aus dem Frankenwald',
 		'Shannon', 'Shepody', 'Sieglinde', 'Siikli', 'Sini', 'Spunta', 'Sirtema', 'Stemster', 'Súper Chola', 'Suvi', 'Sylvana', 'Turbo',
 		'Ukama', 'Fin de Siècle', 'Vales Sovereign', 'Valor', 'Van Gogh', 'Velox', 'Venla', 'Victoria', 'Vital', 'Vitelotte noire', 'Vivaldi',
 		'Wilja', 'Yukon Gold']


def is_valid(target):
	""" Checks if a string is a valid IRC nick. """
	if nick_re.match(target):
		return True
	else:
		return False

@hook.on_start()
def load_foods(bot):
	"""
	:type bot: cloudbot.bot.CloudBot
	"""
	global sandwich_data, taco_data

	with codecs.open(os.path.join(bot.data_dir, "sandwich.json"), encoding="utf-8") as f:
		sandwich_data = json.load(f)

	with codecs.open(os.path.join(bot.data_dir, "taco.json"), encoding="utf-8") as f:
		taco_data = json.load(f)


@asyncio.coroutine
@hook.command(permissions=["food"])
def potato(text, action):
	"""<user> - makes <user> a tasty little potato"""
	user = text.strip()

	if not is_valid(user):
		return "Je n'arrive pas à donner une patate à cette personne."

	potato_type = random.choice(potatoes)
	size = random.choice(['moyenne', 'grosse', 'grande', 'gigantesque'])
	flavor = random.choice(['gouteuse', 'super', 'délicieuse', 'bonne'])
	method = random.choice(['cuisine', 'fait frire', 'fait bouillir', 'fait griller'])
	side_dish = random.choice(['une petite salade', 'un peu de crème fraîche', 'un bout de poulet', 'un bol de bacon'])

	action("{} une {} {} patate {} pour {} et la sert avec {}!".format(method, flavor, size, potato_type, user,
																			   side_dish))


@asyncio.coroutine
@hook.command(permissions=["food"])
def cake(text, action):
	"""<user> - gives <user> an awesome cake"""
	user = text.strip()

	if not is_valid(user):
		return "Je n'arrive pas à donner un gateau à cette personne."

	cake_type = random.choice(cakes)
	size = random.choice(['moyen', 'gros', 'gigantesque'])
	flavor = random.choice(['gouteux', 'super', 'délicieux', 'bon'])
	method = random.choice(['prépare', 'donne', 'cuit', 'achète'])
	side_dish = random.choice(['un chocolat chaud', 'une coupe de glace', 'un pot de cookies',
							   'de la sauce au chocolat'])

	action("{} à {} un {} {} gateau {} et le sert avec {}!".format(method, user, flavor, size, cake_type,
																		 side_dish))


@asyncio.coroutine
@hook.command(permissions=["food"])
def cookie(text, action):
	"""<user> - gives <user> a cookie"""
	user = text.strip()

	if not is_valid(user):
		return "Je n'arrive pas à donner un cookie à cette personne."

	cookie_type = random.choice(cookies)
	size = random.choice(['moyen', 'grand', 'gigantesque'])
	flavor = random.choice(['gouteux', 'délectable', 'délicieux', 'bon'])
	method = random.choice(['prépare', 'donne', 'cuit', 'achète'])
	side_dish = random.choice(['un verre de lait', 'un bol de glace', 'un bol de sauce au chocolat'])

	action("{} à {} un {} et {} cookie {} et le sert avec {}!".format(method, user, size, flavor, cookie_type,
																	 side_dish))


@asyncio.coroutine
@hook.command(permissions=["food"])
def sandwich(text, action):
	"""<user> - give a tasty sandwich to <user>"""
	user = text.strip()

	if not is_valid(user):
		return "Je n'arrive pas à donner un sandwich à cette personne."

	generator = textgen.TextGenerator(sandwich_data["templates"], sandwich_data["parts"],
									  variables={"user": user})

	# act out the message
	action(generator.generate_string())

@asyncio.coroutine
@hook.command(permissions=["food"])
def taco(text, action):
	"""<user> - give a taco to <user>"""
	user = text.strip()

	if not is_valid(user):
		return "Je n'arrive pas à donner un taco à cette personne."

	generator = textgen.TextGenerator(taco_data["templates"], taco_data["parts"],
									  variables={"user": user})

	# act out the message
	action(generator.generate_string())
