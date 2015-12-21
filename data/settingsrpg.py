# -*- coding:Utf-8 -*-
# !/usr/bin/env python3.5

# Remember :
"""
Temps :
1 seconde       = 1
1 minute        = 60
1 heure         = 3600
1 journée       = 86400
1 semaine       = 604800
1 mois (30 jrs.)= 2592000
1 an            = 31536000

Couleurs:
"white"
"black"
"dark blue"
"dark green"
"red"
"dark red"
"brown"  # Note: This appears to show up as brown for some clients, dark red for others.
"purple"
"orange"
"yellow"
"green"
"cyan"
"teal"
"blue"
"pink"
"dark gray"
"gray"
"random" # Special keyword, generate a random number.
}
"""

startExp = 0
digTimeLimit = 60  # s
mineTimeLimit = 120  # s
begTimeLimit = 3600  # s

crateFindChance = 3  # %
expBonusChance = 5  # ‰
megaExpBonusChance = 1  # ‰

objets = {"terre":
              {"diggable": True, "digChance": 90, "minDig": 1, "maxDig": 32,
               "minage": False,
               "four": True, "fourGive": "poussiere", "tempsCuisson": 200,
               "plante": False,
               "caisse": True, "caisseWin": 256,
               "couleur": "brown"},
          "clé":
              {"diggable": True, "digChance": 2, "minDig": 1, "maxDig": 3,
               "minage": False,
               "four": True, "fourGive": "fer", "tempsCuisson": 500,
               "plante": False,
               "caisse": True, "caisseWin": 2,
               "couleur": "gray"},
          "fraise":
              {"diggable": True, "digChance": 10, "minDig": 3, "maxDig": 5,
               "minage": False,
               "four": True, "fourGive": "confiture", "tempsCuisson": 500,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "red"},
          "confiture":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 6,
               "couleur": "dark red"},
          "eau":
              {"diggable": True, "digChance": 90, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "vapeur d'eau", "tempsCuisson": 200,
               "plante": False,
               "caisse": True, "caisseWin": 5,
               "couleur": "blue"},
          "vapeur d'eau":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "vapeur d'eau", "tempsCuisson": 30,
               "plante": False,
               "caisse": False,
               "couleur": "white"},
          "pomme":
              {"diggable": True, "digChance": 20, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "pomme cuite", "tempsCuisson": 60,
               "plante": False,
               "caisse": True, "caisseWin": 13,
               "couleur": "yellow"},
          "pomme cuite":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "pomme cramée", "tempsCuisson": 60,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "brown"},
          "pomme cramée":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "poussiere", "tempsCuisson": 120,
               "plante": False,
               "caisse": True, "caisseWin": 5,
               "couleur": "black"},
          "couteau":
              {"diggable": True, "digChance": 2, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "fer", "tempsCuisson": 60,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "dark gray"},
          "piece de 1€":
              {"diggable": True, "digChance": 5, "minDig": 1, "maxDig": 2,
               "minage": False,
               "four": True, "fourGive": "or", "tempsCuisson": 260,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "yellow"},
          "brindilles":
              {"diggable": True, "digChance": 90, "minDig": 1, "maxDig": 20,
               "minage": False,
               "four": True, "fourGive": "cendre", "tempsCuisson": 100,
               "plante": False,
               "caisse": True, "caisseWin": 128,
               "couleur": "brown"},
          "cendre":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 4,
               "couleur": "gray"},
          "dechets":
              {"diggable": True, "digChance": 85, "minDig": 1, "maxDig": 20,
               "minage": False,
               "four": True, "fourGive": "pollution", "tempsCuisson": 100,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "brown"},
          "pollution":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": False,
               "couleur": "dark"},
          "petrole":
              {"diggable": False,
               "minage": True, "mineChance": 5, "minMine": 1, "maxMine": 1,
               "four": True, "fourGive": "plastique", "tempsCuisson": 100,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "dark"},
          "plastique":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 12,
               "couleur": "green"},
          "bois":
              {"diggable": True, "digChance": 90, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "charbon", "tempsCuisson": 300,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "brown"},
          "corps":
              {"diggable": False,
               "minage": True, "mineChance": 1, "minMine": 1, "maxMine": 1,
               "four": True, "fourGive": "cendre", "tempsCuisson": 200,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "gray"},
          "gravier":
              {"diggable": True, "digChance": 60, "minDig": 1, "maxDig": 32,
               "minage": True, "mineChance": 20, "minMine": 1, "maxMine": 5,
               "four": True, "fourGive": "gravier", "tempsCuisson": 5,
               "plante": False,
               "caisse": True, "caisseWin": 5,
               "couleur": "dark gray"},
          "herbe":
              {"diggable": True, "digChance": 100, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "paille", "tempsCuisson": 5,
               "plante": True, "planteGive": "blé", "tempsPousse": 15,
               "caisse": True, "caisseWin": 3,
               "couleur": "green"},
          "blé":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "pain", "tempsCuisson": 500,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "yellow"},
          "pain":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "pain grillé", "tempsCuisson": 50,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "brown"},
          "pain grillé":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "brown"},
          "paille":
              {"diggable": False,
               "minage": False,
               "four": True, "fourGive": "terre brulee", "tempsCuisson": 5,
               "plante": True, "planteGive": "compost", "tempsPousse": 3600,
               "caisse": True, "caisseWin": 10,
               "couleur": "yellow"},
          "compost":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": True, "planteGive": "engrais", "tempsPousse": 3600,
               "caisse": True, "caisseWin": 1,
               "couleur": "brown"},
          "engrais":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "black"},
          "terre brulee":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 3,
               "couleur": "black"},
          "bague":
              {"diggable": True, "digChance": 5, "minDig": 1, "maxDig": 1,
               "minage": False,
               "four": True, "fourGive": "saphyr", "tempsCuisson": 86400,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "yellow"},
          "pierre":
              {"diggable": True, "digChance": 50, "minDig": 2, "maxDig": 2,
               "minage": True, "mineChance": 90, "minMine": 1, "maxMine": 32,
               "four": False,
               "plante": False,
               "caisse": False,
               "couleur": "dark gray"},
          "charbon":
              {"diggable": False,
               "minage": True, "mineChance": 30, "minMine": 1, "maxMine": 5,
               "four": True, "fourGive": "poussiere", "tempsCuisson": 300,
               "plante": False,
               "caisse": False,
               "couleur": "black"},
          "poussiere":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "gray"},
          "fer":
              {"diggable": False,
               "minage": True, "mineChance": 25, "minMine": 1, "maxMine": 3,
               "four": True, "fourGive": "acier", "tempsCuisson": 3600,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "gray"},
          "cuivre":
              {"diggable": False,
               "minage": True, "mineChance": 25, "minMine": 1, "maxMine": 3,
               "four": True, "fourGive": "cuivre liquide", "tempsCuisson": 3000,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "orange"},
          "cuivre liquide":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 3,
               "couleur": "orange"},
          "or":
              {"diggable": False,
               "minage": True, "mineChance": 10, "minMine": 1, "maxMine": 30,
               "four": True, "fourGive": "or liquide", "tempsCuisson": 3600,
               "plante": False,
               "caisse": True, "caisseWin": 5,
               "couleur": "yellow"},
          "sable":
              {"diggable": True, "digChance": 30, "minDig": 2, "maxDig": 2,
               "minage": True, "mineChance": 30, "minMine": 1, "maxMine": 3,
               "four": True, "fourGive": "verre", "tempsCuisson": 60,
               "plante": False,
               "caisse": True, "caisseWin": 30,
               "couleur": "yellow"},
          "or liquide":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 3,
               "couleur": "orange"},
          "verre":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "teal"},
          "acier":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 10,
               "couleur": "gray"},
          "diamant":
              {"diggable": False,
               "minage": True, "mineChance": 7, "minMine": 1, "maxMine": 1,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 100,
               "couleur": "blue"},
          "emeraude":
              {"diggable": False,
               "minage": True, "mineChance": 5, "minMine": 1, "maxMine": 1,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "green"},
          "saphyr":
              {"diggable": False,
               "minage": True, "mineChance": 2, "minMine": 1, "maxMine": 1,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "purple"},
          "rubis":
              {"diggable": False,
               "minage": True, "mineChance": 1, "minMine": 1, "maxMine": 1,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "red"},
          "caisse":  # ouvrir avec une clé
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": False,
               "couleur": "brown"},
          "seconde":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": True, "caisseWin": 1,
               "couleur": "purple"},
          "charisme":
              {"diggable": False,
               "minage": False,
               "four": False,
               "plante": False,
               "caisse": False,
               "couleur": "purple"},
          }
