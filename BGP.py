import json
import ipaddress
from adresses import get_reseaux_routeur
def annonce_reseau(routeur_iteration,routeur_sur_lequel_on_applique,reseau,commandes):
	"""
	très similaire à la fonction en dessous mais n'annonce que le réseau mis en paramètre
	"""
	if routeur_iteration==routeur_sur_lequel_on_applique:
		commandes.append(f"network {reseau}")

		pass


	pass

def annonce_reseaux_routeur(routeur_sur_lequel_on_applique,commandes,config_noeuds):
	"""
	annnonce tous les réseaux auxquels est connecté le routeur considéré:
	routeur_iteration: le routeur auquel on est à l'itération donnée (on ne veut pas forcément le configurer, on veut configurer le 2e routeur)
	le nom est explicite là
	commandes: la liste des commandes à laquelle on va append
	config_noeuds: voir plus bas si nécessaire pour comprendre
	"""
	
	reseaux=get_reseaux_routeur(routeur_sur_lequel_on_applique,config_noeuds)
	for reseau in reseaux:
		commandes.append(f"network {reseau}")

		



def config_bgp(routeur,voisin,reseau_officiel,router_id,address_ipv6,address_voisin,policy,config_noeuds):
	"""
	router : string
	voisin du routeur : string
	data : dictionnaire contenant les infos json
	router_id : X.X.X.X string
	address_ipv6 : 2001:{numass}:{numreseau}::{i+1}/64 string
	
	"""
	exi=True
	AS = get_as_for_router(routeur,reseau_officiel)
	commandes = [f"router bgp {AS}", "no bgp default ipv4-unicast",f"bgp router-id {router_id}"]
	voisin_as = get_as_for_router(voisin, reseau_officiel)
	# Créer un objet IPv6Network
	if "/" in address_voisin:
		ipv6_noprefix = address_voisin[:address_voisin.index("/")] #sans prefixe, ici ça ne fonctionne pas, pas d'attribut ip
	else:
		ipv6_noprefix=address_voisin
	memeAs=sameAS(routeur,voisin,reseau_officiel)
	if  memeAs and "db8" in ipv6_noprefix: #iBGP, on ne veut garder que les adresses loopback
		commandes.append(f"neighbor {ipv6_noprefix} remote-as {AS}") #en fait c'est l'adresse ipv6 du voisin!!
		commandes.append(f"address-family ipv6 unicast")
		commandes.append(f"neighbor {ipv6_noprefix} activate")
		
	elif not memeAs: #eBGP
		commandes.append(f"neighbor {ipv6_noprefix} remote-as {voisin_as}") #change AS
		commandes.append(f"address-family ipv6 unicast")
		commandes.append(f"neighbor {ipv6_noprefix} activate")
	else: 
		exi=False
		#on ignore, quand ça ne correspond à aucun des cas ci-dessus (on ne veut pas établir iBGP sur les interfaces)
	

	# Créer un objet IPv6Network
	network = ipaddress.IPv6Network(address_ipv6, strict=False)

	# Extraire l'adresse IPv6 et le préfixe
	adresse_reseau = str(network.network_address)
	prefixe = network.prefixlen
	if exi:
		if routeur in reseau_officiel[str(AS)]["annonce_reseaux"]:
			annonce_reseaux_routeur(routeur,commandes,config_noeuds)

		
		
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


def spread_loopback_iBGP(voisin,routeur,reseau_officiel,router_id,address_ipv6,adresse_voisin,policy,config_noeuds):#ici l'adresse voisin est bien sa @loop_voisin!
	"""
	configure l'iBGP pour les routeurs voisins du même AS
	voisin: routeur voisin
	routeur: routeur que l'on configure
	router_id: X.X.X.X 
	le reste est assez explicite
	policy: booléen: True si on utilise le graphe des policies
	config_noeuds: dictionnaire de configuration qui contient les ip et nom d'interfaces
	"""
	commandes=["conf t"]
	if sameAS(routeur,voisin,reseau_officiel): #si c'est dans meme AS on spread @loopback
		commandes.extend(config_bgp(routeur,voisin,reseau_officiel,router_id,address_ipv6,adresse_voisin,policy,config_noeuds))
		commandes.append("exit")
		commandes+=["configure termi",f"router bgp {get_as_for_router(routeur,reseau_officiel)}",f"neighbor {adresse_voisin} remote-as {get_as_for_router(routeur,reseau_officiel)}",f"neighbor {adresse_voisin} update-source Loopback0","exit","exit"]
	return commandes

def config_bgp_routeur(routeur, reseau_officiel,routeur_iden,config_noeud,policy):
	"""
	génère les commandes BGP pour configurer un routeur:
	routeur: le routeur que l'on configure
	reseau_officiel: graphe du réeau (fichier d'intention)
	routeur_iden: id du routeur (pk en ?)
	condig_noeud: le dictionnaire qui contient les infos de config, ip entre autres
	"""
	dico_voisins = config_noeud[routeur]["ip_et_co"]
	
	commandes = ["conf t"]
	for voisin,liste in dico_voisins.items():
		ip_voisin=config_noeud[voisin]["ip_et_co"][routeur][1] #on récupère l'ip du voisin connecté à notre routeur
		commandes.extend(config_bgp(routeur,voisin,reseau_officiel,routeur_iden, liste[1],ip_voisin,policy,config_noeud))
		if policy:
			commandes.extend(policies(routeur, voisin, reseau_officiel, ip_voisin))
	
	commandes.append("exit")
	return commandes

def get_relation(as_number_to_config, as_number_neighbor, data):
	"""
	permet de récupérer les relations type clients/peers/providers depuis le graphe data (fichier d'intention, jsp pourquoi il change de nom à chaque fonction)
	as_number_to_config: le num de l'AS du routeur que l'on est en train de configurer
	as_number_neighbor: le num de l'AS du routeur voisin pour lequel on veut établir les route maps
	"""
	as_number_to_config = str(as_number_to_config)
	as_number_neighbor=str(as_number_neighbor) #le test ne fnctionnait pas dans la liste, c'était un string
	relations = data[as_number_to_config].get('relation', {}) #la clé s'appelle relation pas relations
	for type, as_list in relations.items():
		if as_number_neighbor in as_list:
			return type

def policies(routeur, voisin, data, address_ipv6_neighbor):
	"""
	Crée les commandes de policies pour un routeur donné, un routeur voisin donné,
	data: graphe (fichier d'intention)
	le dernier paramètre est assez explicite
	
	""" 
	as_number = get_as_for_router(routeur, data)
	as_voisin = get_as_for_router(voisin, data)
	commandes = [f"router bgp {as_number}", "address-family ipv6 unicast"]
	if "/" in address_ipv6_neighbor:
		address_ipv6_neighbor = address_ipv6_neighbor[:address_ipv6_neighbor.index("/")] 
	if as_number != as_voisin:
		relation = get_relation(as_number, as_voisin, data)
		if relation == 'provider':
			commandes.append(f"neighbor {address_ipv6_neighbor} route-map PROVIDER in") #pas sûr de mon changement
			commandes.append(f"neighbor {address_ipv6_neighbor} route-map CUSTOMERS_ONLY out")
		elif relation == 'peer':
			commandes.append(f"neighbor {address_ipv6_neighbor} route-map PEER in")
			commandes.append(f"neighbor {address_ipv6_neighbor} route-map CUSTOMERS_ONLY out")
		else:
			commandes.append(f"neighbor {address_ipv6_neighbor} route-map CUSTOMER in")

		commandes.append("exit")
		commandes.append("exit")

		for name, value, tag in (("CUSTOMER", "200", f"{as_number}:200"), ("PEER", "150", f"{as_number}:150"), ("PROVIDER", "100", f"{as_number}:100")):
			commandes.append(f"route-map {name} permit 10")
			commandes.append(f"set local-preference {value}")
			commandes.append(f"set community {tag} additive")

		commandes.append("exit")
		commandes.append(f"ip community-list standard BLOCK permit {as_number}:100")
		commandes.append(f"ip community-list standard BLOCK permit {as_number}:150")
		commandes.append("route-map CUSTOMERS_ONLY deny 10")
		commandes.append("match community BLOCK")
		commandes.append("exit")
		commandes.append("route-map CUSTOMERS_ONLY permit 20")
		commandes.append("exit")
	
	return commandes 

def config_iBGP(routeur,reseau_officiel,router_id,config_noeud,numas,policy):
	"""
	configure iBGP pour un routeur donné,
	reseau_officiel: fichier d'intention
	config_noeud: contient plusieurs données de config dont les adresses ip notemment
	numas: le numéro de l'as,
	router_id: l'id du routeur X.X.X.X
	policy: booléen: si on applique les policies (pour que ça fonctionne même avec le réseau de départ)
	"""
	adresse_self=config_noeud[routeur]["loopback"]
	voisins=reseau_officiel[numas]["routeurs"] #les voisins iBGP sont les mêmes routeurs du réseau
	commandes=[]
	for voisin in voisins.keys():
		if routeur != voisin: #on ne veut pas configurer le routeur lui-même comme voisin
			adresse_voisin=config_noeud[voisin]["loopback"]
			commandes+=spread_loopback_iBGP(voisin,routeur,reseau_officiel,router_id,adresse_self,adresse_voisin,policy,config_noeud)
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
if __name__=="__main__":
	test()

