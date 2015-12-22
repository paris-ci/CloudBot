# -*- coding:Utf-8 -*-
# !/usr/bin/env python3.5
import json
import os
import random
import time

from data.settingsrpg import *

accessList = []


def createProfile(nick):
    foldername = "data/users/" + nick + "/"
    if not os.path.exists(os.path.dirname(foldername)):
        os.makedirs(os.path.dirname(foldername))
    with open(foldername + "account.json", "w") as f:
        f.write("{}")
    with open(foldername + "stats.json", "w") as f:
        f.write("{}")
    with open(foldername + "timers.json", "w") as f:
        f.write("{}")
    with open(foldername + "inventory.json", "w") as f:
        f.write("{}")
    with open(foldername + "settings.json", "w") as f:
        f.write("{}")


def setValue(file, dict_tochange):
    global accessList
    i = 0
    while "data/users/" + file in accessList:
        print("Waiting for file access in data/users/" + file)
        print("---> File access list : " + str(accessList))
        time.sleep(0.5)
        i += 1
        if i > 20:
            accessList = []

    accessList.append("data/users/" + file)
    with open("data/users/" + file, "r") as f:
        dict = json.load(f)
    for index in dict_tochange:
        dict[index] = dict_tochange[index]
    with open("data/users/" + file, "w") as f:
        json.dump(dict, f)
    accessList.remove("data/users/" + file)


def getValue(file, index, default=None):
    global accessList
    i = 0
    while "data/users/" + file in accessList:
        print("Waiting for file access in data/users/" + file)
        print("---> File access list : " + str(accessList))
        i += 1
        if i > 20:
            accessList = []
    accessList.append("data/users/" + file)

    try:
        with open("data/users/" + file, "r") as f:
            dict = json.load(f)

        dict[index]
        accessList.remove("data/users/" + file)
        return dict[index]


    except KeyError:
        if default is not None:
            accessList.remove("data/users/" + file)
            setValue(file, {index: default})
            return default
        else:
            raise


def checkObjetInventaire(nick, objet, nombreMini=0):
    if getValue(nick + "/inventory.json", objet) <= nombreMini:
        return False

    return True


def removeFromInv(nick, objet, nombre=1):
    if checkObjetInventaire(nick, objet, nombre):
        setValue(nick + "/inventory.json", {objet: int(getValue(nick + "/inventory.json", objet, 1)) - nombre})
        return True
    else:
        return False


def addToInv(nick, objet, nombre=1):
    setValue(nick + "/inventory.json", {objet: int(getValue(nick + "/inventory.json", objet, 1)) + nombre})


def rollCrate(nick, notice):
    chance = random.randrange(0, 101)
    if chance <= crateFindChance:
        notice("... En revenant a son campement, " + nick + " trouves aussi une caisse ! Bravo !")
        setValue(nick + "/inventory.json", {"caisse": int(getValue(nick + "/inventory.json", "caisse", 1)) + 1})
        return None

    chance = random.randrange(0, 1001)
    if chance <= megaExpBonusChance:
        expWin = random.randrange(250, 10000)
        setValue(nick + "/stats.json", {"exp": int(getValue(nick + "/stats.json", "exp", startExp)) + expWin})
        notice(
            "... En revenant a son campement, " + nick + " tombes sur un mage, qui lui apprends des sorts! Il gagne " + str(
                expWin) + " points d'experience!")
    elif chance <= expBonusChance:
        expWin = random.randrange(25, 250)
        setValue(nick + "/stats.json", {"exp": int(getValue(nick + "/stats.json", "exp", startExp)) + expWin})
        notice(
            "... En revenant a son campement, " + nick + " tombes sur l'enfant d'un mage, qui lui apprends des sorts! Il gagne " + str(
                expWin) + " points d'experience!")
