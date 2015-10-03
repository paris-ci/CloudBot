import json

import requests

from cloudbot import hook
from cloudbot.util.colors import parse


@hook.command(autohelp=False)
def mcstatus():
	"""- gets the status of various Mojang (Minecraft) servers"""

	try:
		request = requests.get("http://status.mojang.com/check")
		request.raise_for_status()
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		return "Unable to get Minecraft server status: {}".format(e)

	# lets just reformat this data to get in a nice format
	data = json.loads(request.text.replace("}", "").replace("{", "").replace("]", "}").replace("[", "{"))
	out = []

	# use a loop so we don't have to update it if they add more servers
	green = []
	yellow = []
	red = []
	for server, status in list(data.items()):
		if status == "green":
			green.append(server)
		elif status == "yellow":
			yellow.append(server)
		else:
			red.append(server)

	if green:
		green.sort()
		out.append("\x02Online\x02: $(dark_green)" + ", ".join(green) + "$(clear)")
	if yellow:
		yellow.sort()
		out.append("\x02Issues\x02: $(orange)" + ", ".join(yellow) + "$(clear)")
	if red:
		red.sort()
		out.append("\x02Offline\x02: $(dark_red)" + ", ".join(red) + "$(clear)")

	out = parse(" ".join(out))

	return "\x0f" + out.replace(".mojang.com", ".mj") \
		.replace(".minecraft.net", ".mc")
