#!/usr/bin/env python
import hashlib
import re
from urllib.request import FancyURLopener

from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens

HASH_REGEX = re.compile("([a-fA-F0-9]{32})")


class MyOpener(FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


def dictionary_attack(h, wordlist):
	for word in wordlist:
		if str(hashlib.md5(word.encode()).hexdigest()) == str(h):
			return word

	return None


def format_it(hash, plaintext):
	return "{hash}:{plaintext}".format(hash=hash, plaintext=plaintext)


def crack_single_hash(h):
	myopener = MyOpener()
	response = myopener.open(
		"http://www.google.com/search?q={hash}".format(hash=h))

	wordlist = str(response.read()).replace('.', ' ').replace(':', ' ').replace('?', '').replace("('", ' ').replace("'",
	                                                                                                                ' ').split(
		' ')
	plaintext = dictionary_attack(h, set(wordlist))

	return plaintext


class BozoCrack(object):
	def __init__(self, filename):
		self.hashes = []

		with open(filename, 'r') as f:
			hashes = [h.lower() for line in f if HASH_REGEX.match(line)
			          for h in HASH_REGEX.findall(line.replace('\n', ''))]

		self.hashes = sorted(set(hashes))

		#        print "Loaded {count} unique hashes".format(count=len(self.hashes))

		self.cache = self.load_cache()

	def crack(self):
		cracked_hashes = []
		for h in self.hashes:
			if h in self.cache:
				#                print format_it(h, self.cache[h])
				cracked_hashes.append((h, self.cache[h]))
				continue

			plaintext = crack_single_hash(h)

			if plaintext:
				#                print format_it(h, plaintext)
				self.cache[h] = plaintext
				self.append_to_cache(h, plaintext)
				cracked_hashes.append((h, plaintext))

		return cracked_hashes

	@staticmethod
	def load_cache(filename='cache'):
		cache = {}
		with open(filename, 'a+') as c:
			for line in c:
				hash, plaintext = line.replace('\n', '').split(':', 1)
				cache[hash] = plaintext
		return cache

	@staticmethod
	def append_to_cache(h, plaintext, filename='cache'):
		with open(filename, 'a+') as c:
			c.write(format_it(hash=h, plaintext=plaintext) + "\n")


@hook.command("md5crack", "crackmd5")
def md5crack(notice, text, reply, nick):
	if text is None:
		notice("Syntax : !md5crack the_md5_hash")
		return None

	if getTokens(nick) < 2000:
		notice("You don't have enough tokens to crack a md5 (2000 needed)... Help a little more !")
		return None

	takeTokens(50, nick, notice)

	tocrack = str(text)
	notice('Trying to crack : ' + tocrack)

	output = str(crack_single_hash(tocrack))
	if output == "None":
		reply("Didn't found anything for : " + tocrack)
	else:
		reply("Here's what i've found for " + tocrack + " : " + output)


@hook.command("md5hash", "md5")
def md5hash(text, reply, notice, nick):
	if text is None:
		notice("Syntax : !md5hash word")
		return None
	if getTokens(nick) < 500:
		notice("You don't have enough tokens to hash to a md5 (500 needed)... Help a little more !")
		return None

	takeTokens(5, nick, notice)
	tohash = str(text)
	output = str(hashlib.md5(tohash.encode()).hexdigest())
	reply("Hash of " + tohash + " : " + output)
