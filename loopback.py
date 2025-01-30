"""
module qui sert à générer les adresses de loopback pour les routeurs
"""


import BGP as bgp
# Charger le fichier de configuration du réseau

def configure_loopback_address(index):
	"""
	crée une adresse loopback à partir de l'index (numéro du routeur)
	"""
	return f"2001:db8::{index}"

def configure_looback_addresses(config_noeuds):
	"""
	attribue des adresses loopback à chaque routeur
	config_noeuds: graphe qui contient toutes les ip et interface
	"""
	for routeur in config_noeuds.keys():
		config_noeuds[routeur]["loopback"]=configure_loopback_address(routeur[1:])

def generer_loopback_commandes(routeur,config_noeuds):
	"""
	génère les commandes loopback à appliquer au routeur donné en entrée à l'aide du dictionnaire de config
	"""
	commandes = []
	adresse_loopback = config_noeuds[routeur]["loopback"]
	config_noeuds[routeur]["loopback"]=adresse_loopback
	commandes.extend([
                     "conf t",
					f"interface loopback0",
					
					f" ipv6 address {adresse_loopback}/128",
					f"no shutdown",
					f" ipv6 enable",
					"exit",])
	
	commandes.append("end")
	return commandes


if __name__=="__name__":
	import json

	with open('reseau_officiel.json', 'r') as file:
		network_data = json.load(file)
