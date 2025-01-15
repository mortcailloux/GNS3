import json

# Charger le fichier de configuration du réseau
with open('reseau_officiel.json', 'r') as file:
    network_data = json.load(file)

def configure_loopback_address(index):
    return f"2001:db8::{index}"

def generer_loopback_commandes(routeur,protocol):
    commandes = []
    index = routeur[1:]
    adresse_loopback = configure_loopback_address(index)
    commandes.extend([
                    f"interface loopback0",
                    f" ipv6 address {adresse_loopback}/128",
                    f"no shutdown",
					f" ipv6 enable",
                    "exit",
                    f"router {protocol}",
                    f" network {adresse_loopback}/128"
                ])
    return commandes