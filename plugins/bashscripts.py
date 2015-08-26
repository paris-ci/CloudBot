from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens

@hook.command("pastebin", "paste")
def pastebin(text, reply):
	if text is None:
		reply("Syntax : !pastebin fichier")
		return None
	reply("Tape : wget -q -O - --post-file " + text + " http://paste.pr0.tips/ et envoies nous le lien !")

@hook.command("cheat", "cheatbash")
def cheat(reply):
	reply("Commande pour l'installation de cheat : wget -O - http://serv.api-d.com/scripts/cheat.bash | bash")