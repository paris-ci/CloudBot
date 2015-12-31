from cloudbot import hook

@hook.regex(r"\.bots")
def bots(message)
    return "Reporting in! [Python] Cloudbot"
