import json
import ipaddress

def annonce_reseau(routeur_iteration,routeur_sur_lequel_on_applique,reseau,commandes):
	if routeur_iteration==routeur_sur_lequel_on_applique:
		commandes.append(f"network {reseau}")

		pass


	pass


def config_bgp(routeur,voisin,data,router_id,address_ipv6):
	"""
	router : string
	voisin du routeur : string
	data : dictionnaire contenant les infos json
	router_id : X.X.X.X string
	address_ipv6 : 2001:{numass}:{numreseau}::{i+1}/64 string
	
	"""
	AS = get_as_for_router(routeur,data)
	commandes = [f"router bgp {AS}", "no bgp default ipv4-unicast",f"bgp router-id {router_id}"]
	voisin_as = get_as_for_router(voisin, reseau_officiel)
	# Créer un objet IPv6Network
	if "/" in address_voisin:
		ipv6_noprefix = address_voisin[:-3] #sans prefixe, ici ça ne fonctionne pas, pas d'attribut ip
	else:
		ipv6_noprefix=address_voisin
	if  sameAS(routeur,voisin,reseau_officiel): #iBGP
		commandes.append(f"neighbor {ipv6_noprefix} remote-as {AS}") #en fait c'est l'adresse ipv6 du voisin!!
		
	else: #eBGP
		commandes.append(f"neighbor {address_ipv6} remote-as {voisin_as}") #change AS

	commandes.append(f"address-family ipv6 unicast")
	commandes.append(f"neighbor {address_ipv6} activate")

	# Créer un objet IPv6Network
	network = ipaddress.IPv6Network(address_ipv6, strict=False)

	# Extraire l'adresse IPv6 et le préfixe
	adresse_reseau = str(network.network_address)
	prefixe = network.prefixlen
	annonce_reseau(routeur,"R1","2001:1:1::/64",commandes) #on annonce seulement le réseau spécifié
	annonce_reseau(routeur,"R11","2001:2:31::/64",commandes)
	
	commandes.append("exit") #problème ici certainement
	commandes.append("exit")
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

def get_relation(as_number_to_config, as_number_neighbor, data):
	as_number_to_config = str(as_number_to_config)
	relations = data[as_number_to_config].get('relations', {})
	for type, as_list in relations.items():
		if as_number_neighbor in as_list:
			return type

def policies(routeur, voisin, data, address_ipv6): 
	commandes = []
	as_number = get_as_for_router(routeur, data)
	as_voisin = get_as_for_router(voisin, data)
	relation = get_relation(as_number, as_voisin, data)
	if relation == 'provider':
		commandes.append(f"neighbor {voisin} route-map PROVIDER in")
		commandes.append(f"neighbor {address_ipv6} route-map CUSTOMERS_ONLY out")
	elif relation == 'peer':
		commandes.append(f"neighbor {address_ipv6} route-map PEER in")
		commandes.append(f"neighbor {address_ipv6} route-map CUSTOMERS_ONLY out")
	else:
		commandes.append(f"neighbor {address_ipv6} route-map CUSTOMER in")

	commandes.append("exit")
	commandes.append("exit")

	for name, value, tag in (("CUSTOMER", "200", f"{as_number}:200"), ("PEER", "150", f"{as_number}:150"), ("PROVIDER", "100", f"{as_number}:100")):
		commandes.append(f"route-map {name} permit 10")
		commandes.append(f"set local-preference {value}")
		commandes.append(f"set community {tag} additive")
	
		commandes.append(f"ip community-list standard BLOCK permit {as_number}:100")
		commandes.append(f"ip community-list standard BLOCK permit {as_number}:150")
		commandes.append("route-map CUSTOMERS_ONLY deny 10")
		commandes.append("match community BLOCK")
		commandes.append("exit")
		commandes.append("route-map CUSTOMERS_ONLY permit 20")
		commandes.append("exit")
	
	return commandes

def config_iBGP(routeur,reseau_officiel,router_id,config_noeud,numas):
	adresse_self=config_noeud[routeur]["loopback"]
	voisins=reseau_officiel[numas]["routeurs"] #les voisins iBGP sont les mêmes routeurs du réseau
	commandes=[]
	for voisin in voisins.keys():
		if routeur != voisin: #on ne veut pas configurer le routeur lui-même comme voisin
			adresse_voisin=config_noeud[voisin]["loopback"]
			commandes+=spread_loopback_iBGP(voisin,routeur,reseau_officiel,router_id,adresse_self,adresse_voisin)
	return commandes

def test():
	with open("GNS3/reseau_officiel.json") as fichier:
		data=json.load(fichier)
	#print("Numéros d'AS pour chaque routeur :")
	# for as_number, as_data in data.items():
	# 	for routeur in as_data["routeurs"]:
	# 		as_num = get_as_for_router(routeur, data)
	# 		print(f"{routeur}: AS {as_num}")
	print(config_bgp("R4","R8",data,"4.4.4.4","2001:168:192::2/64"))

test()

