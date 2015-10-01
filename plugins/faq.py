import json
import difflib

from cloudbot import hook
from cloudbot.util import web


class FuzzyDict(dict):
	"""Provides a dictionary that performs fuzzy lookup"""

	def __init__(self, items=None, cutoff=.6):
		"""Construct a new FuzzyDict instance

		items is an dictionary to copy items from (optional)
		cutoff is the match ratio below which mathes should not be considered
		cutoff needs to be a float between 0 and 1 (where zero is no match
		and 1 is a perfect match)"""
		super(FuzzyDict, self).__init__()

		if items:
			self.update(items)
		self.cutoff = cutoff

		# short wrapper around some super (dict) methods
		self._dict_contains = lambda key: \
			super(FuzzyDict, self).__contains__(key)

		self._dict_getitem = lambda key: \
			super(FuzzyDict, self).__getitem__(key)

	def _search(self, lookfor, stop_on_first=False):
		"""Returns the value whose key best matches lookfor

		if stop_on_first is True then the method returns as soon
		as it finds the first item
		"""

		# if the item is in the dictionary then just return it
		if self._dict_contains(lookfor):
			return True, lookfor, self._dict_getitem(lookfor), 1

		# set up the fuzzy matching tool
		ratio_calc = difflib.SequenceMatcher()
		ratio_calc.set_seq1(lookfor)

		# test each key in the dictionary
		best_ratio = 0
		best_match = None
		best_key = None
		for key in self:

			# if the current key is not a string
			# then we just skip it
			try:
				# set up the SequenceMatcher with other text
				ratio_calc.set_seq2(key)
			except TypeError:
				continue

			# we get an error here if the item to look for is not a
			# string - if it cannot be fuzzy matched and we are here
			# this it is defintely not in the dictionary
			try:
				# calculate the match value
				ratio = ratio_calc.ratio()
			except TypeError:
				break

			# if this is the best ratio so far - save it and the value
			if ratio > best_ratio:
				best_ratio = ratio
				best_key = key
				best_match = self._dict_getitem(key)

			if stop_on_first and ratio >= self.cutoff:
				break

		return (
			best_ratio >= self.cutoff,
			best_key,
			best_match,
			best_ratio)

	def __contains__(self, item):
		"Overides Dictionary __contains__ to use fuzzy matching"
		if self._search(item, True)[0]:
			return True
		else:
			return False

	def __getitem__(self, lookfor):
		"Overides Dictionary __getitem__ to use fuzzy matching"
		matched, key, item, ratio = self._search(lookfor)

		if not matched:
			raise KeyError(
				"'%s'. closest match: '%s' with ratio %.3f" %
				(str(lookfor), str(key), ratio))

		return item

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
	data = FuzzyDict(data)

	try:
		reponse = data[text[0]]

	except:
		reply("Le mot recherché n'as pas été trouvé dans la FAQ ! Cherchez dans la FAQ avec la liste : !listfaq")
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