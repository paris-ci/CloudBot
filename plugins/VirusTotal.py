import json

import urllib.parse
import urllib.request
from cloudbot.util.colors import parse, colorize
from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens


api_key = "20ba822bfe2a8e1c81b5449dd0a181d59c1cc57b2752d0cbfc4f55103e035d36"

def checkVT(hash):
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": hash, "apikey": api_key}
    data = urllib.parse.urlencode(parameters)
    data = data.encode("utf-8")
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    response = response.read().decode("utf-8")
    return json.loads(response)

@hook.command("virustotal", "virus", "vt")
def virhash(text,notice,nick):
    if getTokens(nick) < 1000:
        notice("You don't have enough tokens to check a file on virus total (1000 needed)... Help a little more !")
        return None

    if not text:
        notice("Please specify an hash (md5, sha1, ...) in this command")
        return None

    takeTokens(50, nick, notice)

    hash = str(text)
    parsedDict = checkVT(hash)
    if int(parsedDict["response_code"]) == 1:
        toreply = parse("Last scan did on " + str(parsedDict["scan_date"]) + ". Positives AV : " + str(colorize(parsedDict["positives"], 1, 10)) + "/" + str(parsedDict["total"]) + "\nMore info at : " + str(parsedDict["permalink"]))
    else:
        toreply = "An error occured ! n°" + str(parsedDict["response_code"]) + " : " + str(parsedDict["verbose_msg"])

    return toreply