from cloudbot import hook
# from plugins.usingBot import getTokens, takeTokens

@hook.command("pastebin", "paste")
def pastebin(text, reply):
	if text is None:
		reply("Syntax : !pastebin fichier")
		return None
	reply("Tape : wget -q -O - --post-file " + text + " http://paste.pr0.tips/ et envoies nous le lien !")

@hook.command("Cpastebin", "Cpaste")
def cpastebin(text, reply):
	if text is None:
		reply("Syntax : !pastebin commande")
		return None
	reply("Tape : " + text + " > stdout.txt && wget -q -O - --post-file stdout.txt http://paste.pr0.tips/ && rm stdout.txt et envoies nous le lien !")


@hook.command("cheat", "cheatbash")
def cheat(reply):
	reply("Commande pour l'installation de cheat : wget -O - http://serv.api-d.com/scripts/cheat.bash | bash")


@hook.command("sysinfo")
def sysinfo(reply):
	reply("Tape : wget -O - http://serv.api-d.com/scripts/sysinfo.bash | bash > resultat.txt && wget -q -O - --post-file resultat.txt http://paste.pr0.tips/ && rm resultat.txt et envoies nous le lien !")


@hook.command("screensaver", "screensave")
def screensaver(reply):
	reply("Tape : wget https://raw.githubusercontent.com/pipeseroni/pipes.sh/master/pipes.sh && bash ./pipes.sh -p 5 -f 50 -r 0 -R && rm pipes.sh")

@hook.command("installjava8", "java8")
def cheat(reply):
	reply("Commande pour l'installation de java 8 : wget -O - http://serv.api-d.com/scripts/java.bash | bash")
