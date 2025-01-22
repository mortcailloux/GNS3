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
	if protocol.lower() =="rip": #lower pour eviter la casse
		commandes.extend([f"ipv6 router rip {routeur}",
					 "interface loopback0",
					f"ipv6 rip {routeur} enable"])
	elif protocol.lower() == "ospf":
		commandes.extend([f"ipv6 router ospf {process_id}", #non mais comment tu as un o différent qui fait crash le routeur cisco ??
					"interface loopback0",
					f"ipv6 ospf {process_id} area 0"])
	commandes.append("end")
	return commandes


if __name__=="__name__":
     with open('reseau_officiel.json', 'r') as file:
        network_data = json.load(file)
