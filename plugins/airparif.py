import json

import urllib.request

from cloudbot.util.colors import parse, colorize
from cloudbot import hook

@hook.command("airparif","air")
def airparif(text):

    try:
        arg = text
    except:
        arg = "jour"

    if arg == "hier" :
        url = "http://www.airparif.asso.fr/appli/api/indice?date=hier"
    elif arg == "demain":
        url = "http://www.airparif.asso.fr/appli/api/indice?date=demain"
    else:
        url = "http://www.airparif.asso.fr/appli/api/indice?date=jour"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        response = response.read().decode("utf-8")
        response = json.loads(response)
    except Exception as e:
        return "Aie ! Une erreur est survenue avec l'api de airparif : " + str(e)

    toreply = ""

    try:
        response["indices"]
        toreply = "Pas de données disponibles pour demain avant 11 heures !"
        return toreply

    except:
        pass

    toreply = "Pour le " + response["date"] + " l'indice de pollution est de " + colorize(response["global"]["indice"], 50, 75) + "\n"
    toreply += "No2 : " + colorize(response["no2"]["indice"], 50, 75) + ", o3 : " + colorize(response["o3"]["indice"], 50, 75) + ", pm10 : " + colorize(response["pm10"]["indice"], 50, 75) + "\n"
    toreply += "Plus d'infos sur la carte : " + response["global"]["url_carte"]
    toreply = parse(toreply)
    return toreply
