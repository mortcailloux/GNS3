import json

def config_ripng(routeur,interface):
    """
    configuration de RIP sur routeur(string) relié à voisins(liste)
    à partir du fichier JSON reseau_officiel.json
    """
    commandes = ["config term","ipv6 unicast-routing","ipv6 router rip ripng",
                "redistribute connected"]
    commandes.append(f"interface {interface}")
    commandes.append("ipv6 rip ripng enable")
    commandes.append("exit") # afin de sortir de l'interface du routeur
    commandes.append("exit")#pour sortir de config terminal
    return commandes


#for i in range(len(voisins)):
		# if i ==0: #pour aller d'abord sur FastEthernet
		# 	interface = "FastEthernet0/0" 
		# else:
		# 	interface = f"GigabitEthernet{i}/0"
def rip_voisins(routeur,reseau_officiel):
    dico_voisins = reseau_officiel["1"]["routeurs"][routeur]
    commandes = []
    for interface in dico_voisins.keys():
        commandes.extend(config_ripng(routeur,interface))
    return commandes

def test():
    with open("reseau_officiel.json") as fichier:
        reseau_officiel=json.load(fichier)
    print(rip_voisins("R3",reseau_officiel))
test()