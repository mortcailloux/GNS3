import json

def config_bgp(routeur,voisins,data,router_id,address_ipv6,ipv6_prefixe):
	"""
	router : string
	voisins : list de voisins
	data : dictionnaire contenant les infos json
	router_id : X.X.X.X string
	address_ipv6 : 2001:{numass}:{numreseau}::{i+1}/64 string
	ipv6_prefixe : 2001:{numass}:{numreseau}::/64 string
	"""
	AS = get_as_for_router(routeur,data)
	commandes = [f"router bgp {AS}", "no bgp default ipv4-unicast",f"bgp router-id {router_id}"]
	
	for voisin in voisins:
		voisin_as = get_as_for_router(voisin, data)
		if sameAS: #iBGP
			commandes.append(f"neighbor {address_ipv6} remote-as {AS}")
			
		else: #eBGP
			commandes.append(f"neighbor {address_ipv6} remote-as {voisin_as}") #change AS

		commandes.append(f"address-family ipv6 unicast")
		commandes.append(f"neighbor {address_ipv6} activate")
		commandes.append(f"network {ipv6_prefixe}")
		commandes.append("end")
	return commandes
		

def sameAS(routeur1,routeur2,data):
	"""
	verifie si deux routeurs sont dans le meme AS
	
	return a boolean 
			->True si meme AS
	"""
	as1 = get_as_for_router(routeur1,data)
	as2 = get_as_for_router(routeur2,data)
	return as1==as2

def get_as_for_router(routeur, data):
    """
    Trouve le numéro d'AS pour un routeur donné en parcourant les données JSON
    
    routeur : string
    data : dict, données contenant les informations des AS et des routeurs
    
    Retourne :
        int : numéro d'AS du routeur
    """
    for as_number, as_data in data.items():
        if routeur in as_data["routeurs"]:
            return int(as_number)
    return None  # Retourne None si le routeur n'est pas trouvé

def test():
	with open("reseau_officiel.json") as fichier:
		data=json.load(fichier)
	print("Numéros d'AS pour chaque routeur :")
	for as_number, as_data in data.items():
		for routeur in as_data["routeurs"]:
			as_num = get_as_for_router(routeur, data)
			print(f"{routeur}: AS {as_num}")
	

test()