from cloudbot import hook


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
    reply(
        "Tape : " + text + " > stdout.txt && wget -q -O - --post-file stdout.txt http://paste.pr0.tips/ && rm stdout.txt et envoies nous le lien !")

@hook.command("listdirs", "listdir", "tree", "treelist", "dirtree", "dirlist")
def dirlist(reply):
    reply("Commande pour voir le contenu d'un repertoire : tape")
    reply(
        """find . -not -path '*/\.*' | python -c "import sys as s;s.a=[];[setattr(s,'a',list(filter(lambda p: c.startswith(p+'/'),s.a)))or (s.stdout.write(' '*len(s.a)+c[len(s.a[-1])+1 if s.a else 0:])or True) and s.a.append(c[:-1]) for c in s.stdin]" """)
    reply("Sinon, plus simple : (sudo) apt-get install tree && tree -d")
