import json
import ipaddress

def annonce_reseau(routeur_iteration,routeur_sur_lequel_on_applique,reseau,commandes):
	if routeur_iteration==routeur_sur_lequel_on_applique:
		commandes.append(f"network {reseau}")

		pass


	pass


def config_bgp(routeur,voisin,reseau_officiel,router_id,address_ipv6,address_voisin):
	"""
	router : string
	voisin du routeur : string
	reseau_officiel : dictionnaire contenant le reseau
	config_noeud : dictionnaire contenant adresse, commandes et @loopback
	router_id : X.X.X.X string
	address_ipv6 : 2001:{numass}:{numreseau}::{i+1}/64 string
	
	"""
	AS = get_as_for_router(routeur,reseau_officiel)
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
		commandes.append(f"neighbor {ipv6_noprefix} remote-as {voisin_as}") #change AS, note 2 : adresse ipv6 du voisin

	commandes.append(f"address-family ipv6 unicast")
	commandes.append(f"neighbor {ipv6_noprefix} activate")#adresse ipv6 du voisin


	network = ipaddress.IPv6Network(address_voisin, strict=False)


	# Extraire l'adresse IPv6 et le préfixe
	adresse_reseau = str(network.network_address)
	prefixe = network.prefixlen
	annonce_reseau(routeur,"R1","2001:1:1::/64",commandes) #on annonce seulement le réseau spécifié
	annonce_reseau(routeur,"R11","2001:2:31::/64",commandes)
	
	commandes.append("exit") #problème ici certainement
	commandes.append("exit")
	return commandes
		

def sameAS(routeur1,routeur2,reseau_officiel):
	"""
	verifie si deux routeurs sont dans le meme AS
	
	return a boolean 
			->True si meme AS
	"""
	as1 = get_as_for_router(routeur1,reseau_officiel)
	as2 = get_as_for_router(routeur2,reseau_officiel)
	return as1==as2

def get_as_for_router(routeur, reseau_officiel):
	"""
	Trouve le numéro d'AS pour un routeur donné en parcourant les données JSON
	
	routeur : string
	reseau_officiel : dict, données contenant les informations des AS et des routeurs
	
	Retourne :
		int : numéro d'AS du routeur
	"""
	for as_number, as_data in reseau_officiel.items():
		if routeur in as_data["routeurs"]:
			return int(as_number)
	return None  # Retourne None si le routeur n'est pas trouvé

def config_bgp_routeur(routeur, reseau_officiel,routeur_iden,config_noeud):
    
	dico_voisins = config_noeud[routeur]["ip_et_co"]
	
	commandes = ["conf t"]
	for voisin,liste in dico_voisins.items():
		ip_voisin=config_noeud[voisin]["ip_et_co"][routeur][1] #on récupère l'ip du voisin connecté à notre routeur
		commandes.extend(config_bgp(routeur,voisin,reseau_officiel,routeur_iden, liste[1],ip_voisin))
	
	commandes.append("exit")
	return commandes
############################
##LOOPBACK functions#########


def config_iBGP(routeur,reseau_officiel,router_id,config_noeud,numas):
	adresse_self=config_noeud[routeur]["loopback"]
	voisins=reseau_officiel[numas]["routeurs"] #les voisins iBGP sont les mêmes routeurs du réseau
	commandes=[]
	for voisin in voisins.keys():
		if routeur != voisin: #on ne veut pas configurer le routeur lui-même comme voisin
			adresse_voisin=config_noeud[voisin]["loopback"]
			commandes+=spread_loopback_iBGP(voisin,routeur,reseau_officiel,router_id,adresse_self,adresse_voisin)
	return commandes
	

def spread_loopback_iBGP(voisin,routeur,reseau_officiel,router_id,address_ipv6,adresse_voisin):#ici l'adresse voisin est bien sa @loop_voisin!
	commandes=["conf t"]
	if sameAS(routeur,voisin,reseau_officiel): #si c'est dans meme AS on spread @loopback
		commandes.extend(config_bgp(routeur,voisin,reseau_officiel,router_id,address_ipv6,adresse_voisin))
		commandes.append("exit")
		commandes+=["configure termi",f"router bgp {get_as_for_router(routeur,reseau_officiel)}",f"neighbor {adresse_voisin} remote-as {get_as_for_router(routeur,reseau_officiel)}",f"neighbor {adresse_voisin} update-source Loopback0","exit","exit"]
	return commandes

def test():
    with open("reseau_officiel.json") as fichier:
        reseau_officiel=json.load(fichier)
    # print("Numéros d'AS pour chaque routeur :")
    # for as_number, as_data in reseau_officiel.items():
    #     for routeur in as_data["routeurs"]:
    #         print(routeur+ ":" )
    #         print(get_as_for_router(routeur,reseau_officiel))
    # print(sameAS("R1","R4",reseau_officiel))
    print(config_bgp("R4","R8",reseau_officiel,"4.4.4.4","2001:168:192::2/64"))

if __name__=="__main__":
	test()

