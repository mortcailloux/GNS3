import json
import ipaddress
import BGP as bgp
# Charger le fichier de configuration du réseau

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
                    f"router {protocol}", #commande incomplète 
                    f" network {adresse_loopback}/128"
                ])
    return commandes

def spread_loopback_iBGP(commandes, voisin,routeur,reseau_officiel,router_id,address_ipv6):
    if sameAS(routeur,voisin,reseau_officiel): #si c'est dans meme AS on spread @loopback
        AS=bgp.get_as_for_router(routeur)
        commandes.extend([f"router bgp {AS}", "no bgp default ipv4-unicast",f"bgp router-id {router_id}",
                          f"neighbor {address_ipv6} remote-as {AS}",f"address-family ipv6 unicast",f"neighbor {address_ipv6} activate"]) 
            # Créer un objet IPv6Network
        network = ipaddress.IPv6Network(address_ipv6, strict=False)

        # Extraire l'adresse IPv6 et le préfixe
        adresse_reseau = str(network.network_address)
        prefixe = network.prefixlen
        commandes.append(f"network {adresse_reseau}/{prefixe}")
        commandes.append("end")
        return commandes
    else:
        return None
def sameAS(routeur1,routeur2,reseau_officiel):
	"""
	verifie si deux routeurs sont dans le meme AS
	
	return a boolean 
			->True si meme AS
	"""
	as1 = bgp.get_as_for_router(routeur1,reseau_officiel)
	as2 = bgp.get_as_for_router(routeur2,reseau_officiel)
	return as1==as2


if __name__=="__name__":
     with open('reseau_officiel.json', 'r') as file:
        network_data = json.load(file)
