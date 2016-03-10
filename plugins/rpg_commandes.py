# -*- coding:Utf-8 -*-
# !/usr/bin/env python3.5

import json
import math
import os
import random
import time

import prettytable
from data.settingsrpg import *

import cloudbot.util.web as web
import plugins.rpg_backend as backend
from cloudbot import hook
from cloudbot.util.colors import parse

accessList = []


@hook.command("accesslist", permissions=["rpgadmin"])
def debug_resetfileaccesslist():
    global accessList
    accessList = []
    return "OK"


@hook.command("showtime", "time")
def debug_showTime():
    return time.strftime("%d/%m à %H:%M:%S", time.localtime())


@hook.command("toutfaire", "all", permissions=["rpgadmin"])
def debug_toutfaire(nick, message, notice):
    beg(nick, message, notice)
    time.sleep(1)
    mine(nick, message, notice)
    time.sleep(1)
    dig(nick, message, notice)
    time.sleep(1)
    cuire(nick, message, "sable", notice)


@hook.command("resettimers")
def debug_resettimers(nick, message):
    backend.setValue(nick + "/timers.json", {"digTimer": 1, "begTimer": 1, "mineTimer": 1, "fourTimer": 1})
    message("ok")


############################

@hook.command()
def init(nick, message):
    if not os.path.exists(os.path.dirname("data/users/" + nick + "/")):
        message("Bienvenue " + str(nick) + ". Je vais vous créer un profil !")
        backend.createProfile(nick)
        backend.setValue(nick + "/account.json", {"joinedAt": int(time.time())})
        backend.setValue(nick + "/stats.json", {"exp": startExp})
        message(nick + ", apparait a la lisiere du village. Il est niveau 1, et dispose de " + str(
                startExp) + " points d'experience! ")
    else:
        message("Bonjour " + str(nick) + ". J'ai l'impression que vous avez déjà un profil ;)")


@hook.command("aide", "help", "sos")
def aide(message, notice):
    notice(parse(
            "$(bold)En premier, vous devez vous enregistrer sur le bot : tapez >init sur une channel ou il es présent !$(clear)"))
    notice("N'oubliez pas de proteger votre pseudo avec NickServ ou équivalent !")
    message("L'aide est disponible ici > " + web.paste("""
    Les commandes disponibles sont :
    - Les niveaux :
      >exp => Voir votre experience actuelle
      >levelup => Augmenter de niveau
    - Les actions :
      >inv => Affiche votre inventaire
      >mendier => Mendiez dans la rue, à la recherche d'or
      >creuser => Grattez le sol a la recherche d'objets perdus
      >miner => Minez et trouvez des minerais
      >cuire => Faites chauffer un objet
      >ouvrir => Ouvrez une caisse
      >pute => Tentez la prostitution pour de l'argent
      >planter (bientot) => Plantez des graines
      >ramasser (bientot) => Ramassez une plante
      >tabasser (bientot) => Tentez de tuer une personne
    - Les echanges :
      >donner => Donne un ou plusieurs objets a une personne
      >acheter => Achete sur la place du marché
      >vendre => Vends sur la place du marché
      >marche => Voir les objets en vente sur la place du marché
      >reprendre => Enlevez une de vos offres du marché
      >voler (bientot) => Essaye de voler quelques objets a une personne (attention, dangereux!)
    """))


#############################

@hook.command()
def exp(nick, message, text):
    if text:
        try:
            level = backend.getValue(text + "/stats.json", "level", 1)
            exp = backend.getValue(text + "/stats.json", "exp", startExp)
            expNeeded = int(level + 300 * math.pow(2, float(level) / 7))
        except KeyError:
            message(nick + ", " + text + " ne dispose pas de points d'experience / n'as pas crée son compte!")
            return None
        message(nick + ", " + text + " dispose de " + str(exp) + " points d'experience!")
        if exp > expNeeded:
            message(nick + ", " + text + " peut monter de niveau !")
        else:
            message(nick + ", " + text + " ne peut pas monter en niveau ! Il lui manque " + str(
                    expNeeded - exp) + " points d'experience !")

        message(nick + ", " + text + " es au niveau " + str(level))

    else:
        level = backend.getValue(nick + "/stats.json", "level", 1)
        exp = backend.getValue(nick + "/stats.json", "exp", startExp)
        expNeeded = int(level + 300 * math.pow(2, float(level) / 7))

        message(nick + ", vous avez " + str(exp) + " points d'experience!")
        if exp > expNeeded:
            message(nick + ", vous pouvez monter de niveau !")
        else:
            message(nick + ", vous ne pouvez pas monter en niveau ! Il vous manque " + str(
                    expNeeded - exp) + " points d'experience !")

        message(nick + ", vous etes au niveau " + str(level))


@hook.command("levelup")
def levelup(nick, message):
    level = backend.getValue(nick + "/stats.json", "level", 1)
    exp = backend.getValue(nick + "/stats.json", "exp", startExp)
    expNeeded = int(level + 300 * math.pow(2, float(level) / 7))

    if exp > expNeeded:
        message(
                nick + " augmente de niveau, il devient niveau " + str(level + 1) + " pour " + str(
                        expNeeded) + " exp !")
        backend.setValue(nick + "/stats.json",
                         {"exp": exp - expNeeded, "level": level + 1, "maxObjets": int(1.3 * level) + 2})
        backend.setValue(nick + "/timers.json", {"digTimer": 1, "begTimer": 1, "mineTimer": 1, "fourTimer": 1})
    else:
        message(nick + ", vous ne pouvez pas monter en niveau ! Il vous manque " + str(
                expNeeded - exp) + " points d'experience !")


#############################

@hook.command("creuser", "creuse", "dig")
def dig(nick, message, notice):
    digTimer = backend.getValue(nick + "/timers.json", "digTimer", 1)
    maxObjets = backend.getValue(nick + "/stats.json", "maxObjets", 2)
    if time.time() >= digTimer:
        backend.setValue(nick + "/timers.json", {"digTimer": int(time.time()) + digTimeLimit})
        found = {}
        nombreObjetsTrouves = 0
        for objet in objets:
            chance = random.randrange(0, 101)
            if objets[objet]["diggable"] and objets[objet]["digChance"] > chance:
                if objets[objet]["minDig"] == objets[objet]["maxDig"]:
                    trouve = objets[objet]["maxDig"]
                else:
                    trouve = random.randrange(objets[objet]["minDig"], objets[objet]["maxDig"])

                if trouve is not 0:
                    nombreObjetsTrouves += trouve
                    if nombreObjetsTrouves >= maxObjets:
                        # trouve = trouve - (nombreObjetsTrouves - trouve - maxObjets + trouve)
                        trouve -= nombreObjetsTrouves - maxObjets
                    if trouve <= 0:
                        break
                    found[objet] = trouve
                    backend.addToInv(nick, objet, trouve)

        toreply = nick + ", vous fouillez la terre sous vos pieds, et trouvez..."
        if not found:
            message(toreply + " Strictement rien !")
            return None
        for objet in found:
            toreply += " " + str(found[objet]) + "x $(" + objets[objet]["couleur"] + ")" + objet + "$(clear)"
        toreply += "!"
        message(parse(toreply))
        expGagnee = random.randrange(1, nombreObjetsTrouves ** 2 + 1)
        backend.setValue(nick + "/stats.json",
                         {"exp": int(backend.getValue(nick + "/stats.json", "exp", startExp)) + expGagnee})
        message(parse(nick + ", vous gagnez $(bold)" + str(expGagnee) + "$(clear) points d'experience!"))
        backend.rollCrate(nick, message)
    else:
        tempsRestant = time.strftime("%d/%m à %H:%M:%S", time.localtime(digTimer))
        notice(parse(
            nick + ", vous etes trop fatigué pour baisser la tete! C'est l'heure d'aller au lit ! Vous serez reposé le " + tempsRestant + " 1x $(" +
            objets["flemme"]["couleur"] + ")flemme$(clear)"))
        backend.addToInv(nick, "flemme")


@hook.command("miner", "mine")
def mine(nick, message, notice):
    mineTimer = backend.getValue(nick + "/timers.json", "mineTimer", 1)
    maxObjets = backend.getValue(nick + "/stats.json", "maxObjets", 2)
    if time.time() >= mineTimer:
        backend.setValue(nick + "/timers.json", {"mineTimer": int(time.time()) + mineTimeLimit})
        found = {}
        nombreObjetsTrouves = 0
        for objet in objets:
            chance = random.randrange(0, 101)
            if objets[objet]["minage"] and objets[objet]["mineChance"] > chance:
                if objets[objet]["minMine"] == objets[objet]["maxMine"]:
                    trouve = objets[objet]["maxMine"]
                else:
                    trouve = random.randrange(objets[objet]["minMine"], objets[objet]["maxMine"])
                if trouve is not 0:
                    nombreObjetsTrouves += trouve
                    if nombreObjetsTrouves >= maxObjets:
                        # trouve = trouve - (nombreObjetsTrouves - trouve - maxObjets + trouve)
                        trouve -= nombreObjetsTrouves - maxObjets
                    if trouve <= 0:
                        break
                    found[objet] = trouve
                    backend.addToInv(nick, objet, trouve)

        toreply = nick + ", vous creusez dans la montagne, et trouvez..."
        if not found:
            message(toreply + " Strictement rien !")
            return None
        for objet in found:
            toreply += " " + str(found[objet]) + "x $(" + objets[objet]["couleur"] + ")" + objet + "$(clear)"
        toreply += "!"
        message(parse(toreply))
        expGagnee = random.randrange(1, nombreObjetsTrouves ** 2 + 1)
        backend.setValue(nick + "/stats.json",
                         {"exp": int(backend.getValue(nick + "/stats.json", "exp", startExp)) + expGagnee})
        message(parse(nick + ", vous gagnez $(bold)" + str(expGagnee) + "$(clear) points d'experience!"))
        backend.rollCrate(nick, message)
    else:
        tempsRestant = time.strftime("%d/%m à %H:%M:%S", time.localtime(mineTimer))
        notice(parse(
            nick + ", vous etes trop fatigué pour miner! Reprennez des forces, vous serez reposé le " + tempsRestant + " 1x $(" +
            objets["flemme"]["couleur"] + ")flemme$(clear)"))
        backend.addToInv(nick, "flemme")


@hook.command("mendier", "mendie", "beg")
def beg(nick, message, notice):
    begTimer = backend.getValue(nick + "/timers.json", "begTimer", 1)
    diff = time.time() - begTimer
    if diff >= 0:
        backend.setValue(nick + "/timers.json", {"begTimer": int(time.time()) + begTimeLimit})
        level = backend.getValue(nick + "/stats.json", "level", 1)
        trouve = random.randrange(1, level * 15)
        backend.addToInv(nick, "or", trouve)
        message(parse(nick + ", vous mendiez quelques temps, puis un passant vous offre $(yellow)" + str(
                trouve) + "$(clear) d'or."))
    elif diff >= -3:
        message("En partant mendier, vous tombez sur une seconde de moins ! Vous rentrez chez vous !")
        backend.addToInv(nick, "seconde")
    else:
        tempsRestant = time.strftime("%d/%m à %H:%M:%S", time.localtime(begTimer))
        notice(parse(
            nick + ", vous avez trop froid pour partir mendier maintenent! Réchauffez vous jusqu'au " + tempsRestant + " 1x $(" +
            objets["flemme"]["couleur"] + ")flemme$(clear)"))
        backend.addToInv(nick, "flemme")


@hook.command("pute")
def pute(nick, message):
    message(parse(nick + " essaye de se prostituer, mais ca ne marche pas vraiment! -1 $(" + objets["charisme"][
        "couleur"] + ")charisme"))
    backend.removeFromInv(nick, "charisme")


@hook.command("ouvrir", "ouvre")
def ouvre(nick, message):
    nbrecle = backend.getValue(nick + "/inventory.json", "clé", 1)
    nbrecaisse = backend.getValue(nick + "/inventory.json", "caisse", 1)
    if nbrecle > 0 and nbrecaisse > 0:
        backend.setValue(nick + "/inventory.json",
                         {"clé": nbrecle - 1, "caisse": nbrecaisse - 1})  # no remove from inv to speed up
        objet = random.choice(list(objets.keys()))
        if objets[objet]["caisse"]:
            backend.addToInv(nick, objet, objets[objet]["caisseWin"])
            message(parse(
                    "Bravo " + nick + " vous ouvrez la caisse et trouvez : " + str(
                            objets[objet]["caisseWin"]) + "x $(" +
                    objets[objet]["couleur"] + ")" + objet + "$(clear)"))

            objet = random.choice(list(objets.keys()))
            if objets[objet]["caisse"]:
                backend.addToInv(nick, objet, objets[objet]["caisseWin"])
                message(parse(
                        nick + ", vous n'aviez pas vu qu'il restait : " + str(objets[objet]["caisseWin"]) + "x $(" +
                        objets[objet]["couleur"] + ")" + objet + "$(clear) dans cette caisse ?"))

                objet = random.choice(list(objets.keys()))
                if objets[objet]["caisse"]:
                    backend.addToInv(nick, objet, objets[objet]["caisseWin"])
                    message(parse(nick + " ATTENDS! Il y a " + str(objets[objet]["caisseWin"]) + "x $(" + objets[objet][
                        "couleur"] + ")" + objet + "$(clear) collé en dessous de la caisse !"))

        else:
            message(
                    nick + ", il n'y a rien dans cette caisse :'( ! Oooh, c'est trop inzuste ! C'est de la faute aux programmeurs : https://www.youtube.com/watch?v=MYZ67-Sh7kM")
    else:
        message(nick + ", voyons, comment veut tu ouvrir cette caisse sans clé ou cette clé sans caisse ?")


@hook.command("cuire", "cuir", "cuit", "chauffe", "four", "furnace")
def cuire(nick, message, text, notice):
    """[item]"""
    fourTimer = backend.getValue(nick + "/timers.json", "fourTimer", 1)
    objet = text
    try:
        objets[objet]["four"]
    except:
        message(nick + ", cet objet n'existe pas :(")
        return None

    if time.time() >= fourTimer:

        if objets[objet]["four"]:
            try:
                soldeAcutel = backend.getValue(nick + "/inventory.json", objet)
                if soldeAcutel < 1:
                    raise KeyError
                backend.setValue(nick + "/inventory.json", {objet: int(soldeAcutel) - 1, objets[objet]["fourGive"]: int(
                        backend.getValue(nick + "/inventory.json", objets[objet]["fourGive"],
                                         1)) + 1})  # No addtoinv here to speed up multiple access
                backend.setValue(nick + "/timers.json", {"fourTimer": int(time.time()) + objets[objet]["tempsCuisson"]})
                message(parse(
                        nick + ", vous enfournez 1x$(" + objets[objet][
                            "couleur"] + ")" + objet + "$(clear) et trouvez dans le four 1x$(" +
                        objets[objets[objet]["fourGive"]]["couleur"] + ")" +
                        objets[objet]["fourGive"]))

            except KeyError:
                message(nick + ", vous n'avez pas cet item è_é")
        else:
            message(nick + ", vous ne pouvez pas cuire ce genre de choses !")

    else:
        tempsRestant = time.strftime("%d/%m à %H:%M:%S", time.localtime(fourTimer))
        notice(parse(
            nick + ", votre four est trop chaud ! Attendez la fin du cycle de refroidissement, qui sera le " + tempsRestant + " 1x $(" +
            objets["flemme"]["couleur"] + ")flemme$(clear)"))
        backend.addToInv(nick, "flemme")


#############################

@hook.command("inventory", "inv")
def inventory(nick, message, text):
    x = prettytable.PrettyTable(["Objet", "Quantite", "Peut etre cuit", "Peut etre planté"])
    x.padding_width = 1
    if text:
        try:
            with open("data/users/" + text + "/inventory.json", "r") as f:
                dict = json.load(f)

            objetsInInv = []
            for objet in dict:
                objetsInInv.append(objet)
            objetsInInv.sort()
            for objet in objetsInInv:
                if objets[objet]["four"]:
                    cuisson = "x"
                else:
                    cuisson = ""

                if objets[objet]["plante"]:
                    plante = "x"
                else:
                    plante = ""

                x.add_row([objet, str(dict[objet]), cuisson, plante])
            message("Inventaire de " + text + ": " + web.paste(x.get_string()))
            return None

        except:
            message(nick + ", cet utilisateur n'existe pas !")
            return None
    else:
        with open("data/users/" + nick + "/inventory.json", "r") as f:
            dict = json.load(f)

        objetsInInv = []
        for objet in dict:
            objetsInInv.append(objet)
            objetsInInv.sort()

        for objet in objetsInInv:
            if objets[objet]["four"]:
                cuisson = "x"
            else:
                cuisson = ""

            if objets[objet]["plante"]:
                plante = "x"
            else:
                plante = ""
            x.add_row([objet, str(dict[objet]), cuisson, plante])

        message("Votre inventaire: " + web.paste(x.get_string()))
        return None


@hook.command("donner", "donne", "give")
def donner(nick, message, text, notice):
    """<nom> <objet> <quantitée>"""
    text = text.split()
    print(text)
    if nick == text[0]:
        notice(nick + ", te donner des objets a toi meme, quelle idée !")
        return None

    try:
        quentite = int(''.join(text[-1:]))
        objet = ' '.join(text[1:-1])
    except ValueError:
        quentite = 1
        objet = ' '.join(text[1:])

    if quentite < 1:
        notice("Donne quelque chose au moins, radin !")
        return None

    if objet not in objets:
        notice("Cet objet n'existe pas !")
        return None

    if backend.checkObjetInventaire(nick, objet, quentite):
        backend.removeFromInv(nick, objet, quentite)
        backend.addToInv(text[0], objet, quentite)
        message(parse(
                text[0] + ", remercie " + nick + " qui t'as gentiment offert " + str(quentite) + "x $(" + objets[objet][
                    "couleur"] + ")" + objet + "$(clear)"))
    else:
        notice(nick + ", vous n'avez pas " + str(quentite) + "x " + objet + ", ou cet objet n'existe pas ^^")


@hook.command("marche", "pdm")
def marche(nick, message, text):
    global accessList
    i = 0
    while "data/marche.json" in accessList:
        print("Waiting for file access in data/marche.json")
        print("---> File access list : " + str(accessList))
        i += 1
        if i > 20:
            accessList = []
    accessList.append("data/marche.json")

    with open("data/marche.json", "r") as f:
        marche = json.load(f)

    accessList.remove("data/marche.json")

    if text not in ["ID", "Quantite", "Objet", "Prix", "Vendeur"]:
        text = "ID"

    x = prettytable.PrettyTable(["ID", "Quantite", "Objet", "Prix", "Vendeur"])
    x.padding_width = 1

    for objet in marche:
        for vente in marche[objet]:
            x.add_row([int(vente["numero"]), str(vente["quentite"]), str(objet), int(vente["prix"]),
                       str(vente["vendeur"])])

    message("Liste des objets vendus sur le marché: " + web.paste(x.get_string(sortby=text, reversesort=True)))


@hook.command("vendre", "vend", "sell")
def vend(nick, message, text, notice):
    """<quentite> <objet> <prix>"""
    global accessList
    i = 0
    while "data/marche.json" in accessList:
        print("Waiting for file access in data/marche.json")
        print("---> File access list : " + str(accessList))
        i += 1
        time.sleep(0.1)
        if i > 20:
            accessList = []
    accessList.append("data/marche.json")

    with open("data/marche.json", "r") as f:
        marche = json.load(f)

    with open("data/offres_marche_compteur", "r") as f:
        numero = int(f.read())

    with open("data/offres_marche_compteur", "w") as f:
        f.write(str(numero + 1))

    text = text.split()
    try:
        quentite = int(''.join(text[:1]))
        objet = str(' '.join(text[1:-1]))
        prix = int(''.join(text[-1:]))
        if not objet in objets:
            notice(nick + ", l'objet " + str(objet) + " n'existe pas !!")
            accessList.remove("data/marche.json")
            return None
        if not backend.checkObjetInventaire(nick, objet, nombreMini=quentite):
            notice(nick + ", vous n'avez pas assez de " + objet + " pour en vendre (il faut qu'il vous en reste minimum 1 à la fin de la vente !)")
            accessList.remove("data/marche.json")
            return None
        if prix < 0:
            notice(nick + ", tu veux vendre des choses a un prix négatif toi ?")
            accessList.remove("data/marche.json")
            return None

        if quentite <= 0:
            notice(nick + ", tu veux vendre quoi déja ?")
            accessList.remove("data/marche.json")
            return None
    except ValueError:
        notice("Euh... <quentite> <objet> <prix>")
        accessList.remove("data/marche.json")
        return None

    """
    marche > objet1 > [{prix, quentite, vendeur, numero}, {prix, quentitee, vendeur, numero}]
           > objet2 > [{prix, quentite, vendeur, numero}]
    """
    try:
        prev = marche[objet]
    except KeyError:
        prev = []

    marche[objet] = prev + [{"prix": prix, "quentite": quentite, "vendeur": nick, "numero": numero}]

    backend.removeFromInv(nick, objet, quentite)

    message(
            nick + ", vous vendez sur la place du marché " + str(quentite) + "x " + str(
                    objet) + " pour la somme de " + str(
                    prix) + "x or")

    with open("data/marche.json", "w") as f:
        json.dump(marche, f)

    accessList.remove("data/marche.json")


@hook.command("acheter", "achat", "buy")
def acheter(nick, message, text, notice):
    """<numero>"""
    global accessList
    i = 0
    while "data/marche.json" in accessList:
        print("Waiting for file access in data/marche.json")
        print("---> File access list : " + str(accessList))
        i += 1
        time.sleep(0.1)
        if i > 20:
            accessList = []
    accessList.append("data/marche.json")

    text = int(text)

    with open("data/marche.json", "r") as f:
        marche = json.load(f)

    for objet in marche:
        for offre in marche[objet]:
            if offre["numero"] == text:
                if backend.checkObjetInventaire(nick, "or", nombreMini=offre["prix"]):
                    backend.removeFromInv(nick, "or", nombre=offre["prix"])
                    backend.addToInv(offre["vendeur"], "or", offre["prix"])
                    backend.addToInv(nick, objet, offre["quentite"])

                    marche[objet].remove(offre)
                    with open("data/marche.json", "w") as f:
                        json.dump(marche, f)

                    accessList.remove("data/marche.json")
                    message(nick + " achete " + str(offre["quentite"]) + "x " + str(objet) + " sur la place du marché à " + str(offre["vendeur"]) + " pour " + str(offre["prix"]) + "x or ! C'est de la bonne qualitée !")
                    return None
                else:
                    notice(nick + ", vous n'avez pas " + str(offre["prix"]) + "x or !")
                    accessList.remove("data/marche.json")

    notice(nick + ", cette offre n'existe pas !")
    accessList.remove("data/marche.json")


@hook.command("reprendre", "takeback", "tb")
def reprendre(nick, message, text, notice):
    """<numero>"""
    global accessList
    i = 0
    while "data/marche.json" in accessList:
        print("Waiting for file access in data/marche.json")
        print("---> File access list : " + str(accessList))
        i += 1
        time.sleep(0.1)
        if i > 20:
            accessList = []
    accessList.append("data/marche.json")

    text = int(text)

    with open("data/marche.json", "r") as f:
        marche = json.load(f)

    for objet in marche:
        for offre in marche[objet]:
            if offre["numero"] == text:
                if offre["vendeur"] == nick:
                    backend.addToInv(offre["vendeur"], objet, offre["quentite"])

                    marche[objet].remove(offre)
                    with open("data/marche.json", "w") as f:
                        json.dump(marche, f)

                    accessList.remove("data/marche.json")
                    message(nick + ", offre suprimée!")
                    return None
                else:
                    notice(nick + ", ce n'est pas votre offre !")
                    accessList.remove("data/marche.json")
                    return None

    notice(nick + ", cette offre n'existe pas !")
    accessList.remove("data/marche.json")
    return None
