__author__ = 'arthur'
import urllib.request

import yaml

from cloudbot import hook


@hook.command("yamlparse", "yamlsyntax", "ymlsyntax", "ymlparse", "checkyaml", "checkyml")
def parseyaml(reply, text):
    try:
        doc = urllib.request.urlopen(text).read()
    except urllib.request.URLError:
        reply("Invalid URL!")
        return

    try:
        yaml.safe_load(doc)
    except Exception as e:
        reply(
                "An error occured while trying to parse your document. Check if the url is valid and contains only your document. Check syntax for errors too (tabs/spaces?).")
        reply("The exeption was : " + str(e))
        return None

    reply("Everything seems fine in this document !")
