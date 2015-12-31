from cloudbot import hook

@hook.regex(r"\.bots")
def bots()
    return "Reporting in! [Python] Cloudbot"
