import json
import ipaddress
import BGP as bgp
# Charger le fichier de configuration du réseau

def configure_loopback_address(index):
	return f"2001:db8::{index}"

def configure_looback_addresses(config_noeuds):
	for routeur in config_noeuds.keys():
		config_noeuds[routeur]["loopback"]=configure_loopback_address(routeur[1:])

def generer_loopback_commandes(routeur,protocol,process_id,config_noeuds):
	commandes = []
	index = routeur[1:]
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
     with open('reseau_officiel.json', 'r') as file:
        network_data = json.load(file)
