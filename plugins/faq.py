from cloudbot import hook
@hook.command("faq")
def faq(text, reply, notice):
	reponses = {
		"faq": "Utilisez la faq avec la commande !faq",
		"donnermonip": """"J'ai ton adresse postale, je peux faire quoi ? T'envoyer une lettre, c'tout. Ton adresse ip je peux t'envoyer des paquets, et encore, y'a un firewall". \n Aucun risque a donner ton IP !""",
		"but_why": "BUT WHYYYY ? > http://bit.ly/1CHRlDF",
		"bot": "Je suis un bot, tu peux voir ce que je sais faire en tapant !help",
		"p1": "Port TCPMUX",
		"p7": "Port ICMP/echo (ping)",
		"p20": "Port ftp (ftp://) (https://tools.ietf.org/html/rfc2577)",
		"p21": "Port ftp (https://tools.ietf.org/html/rfc2577)",
		"p22": "Port ssh",
		"p23": "Port telnet",
		"p25": "Port SMTP (envoi d'e-mails)",
		"p53": "Port DNS",
		"p80": "Port web (http://)",
		"p110": "Port pop3",
		"p119": "Port NNTP",
		"p143": "Port IMAP",
		"p194": "Port IRC",
		"p443": "Port web (https://)",
		"p465": "Port SMTPS (envoi d'e-mails)",
		"p25565": "Port des serveurs minecraft par défaut"
	}

	text = text.split()

	try:
		reponse = reponses[text[0]]

	except:
		reply("Le mot recherché n'as pas été trouvé dans la FAQ !")
		return


	try:
		notice(reponse, text[1])
		notice("Transmis !")

	except:
		reply(reponse)
