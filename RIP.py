import json

def config_ripng(routeur, voisins):
	"""
	configuration de RIP sur routeur(string) relié à voisins(liste)
	à partir du fichier JSON reseau_officiel.json
	"""
	commandes = ["config term","ipv6 unicast-routing","ipv6 router rip ripng"
			  "redistribute connected"]
	for voisin in voisins:
		interface = f"FastEthernet0/{voisins.index(voisin)}" # je sais pas comment automatiser la config des interfaces
		commandes.append(f"interface {interface}")
		commandes.append("ipv6 rip ripng enable")
		commandes.append("exit") # afin de sortir de l'interface du routeur
	commandes.append("exit")#pour sortir de config terminal

	print(f"configuration pour le routeur {routeur}")

	input("souhaites-tu connaître")