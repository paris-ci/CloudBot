from cloudbot import hook

@hook.regex(r"^\.bots")
def bots(message):
    message("Reporting in! [Python] Cloudbot")
