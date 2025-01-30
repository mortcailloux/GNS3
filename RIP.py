"""
module qui sert à générer les commandes qui configurent rip sur le routeur
"""


def config_ripng(interface):
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
def config_rip_routeur(routeur,reseau_officiel,numAs):
    """configure toutes les interfaces d'un routeur donné
    routeur: routeur considéré
    reseau_officiel: graphe du réseau (fichier d'intention)
    numAs: numéro de l'AS du routeur
    """
    dico_voisins = reseau_officiel[numAs]["routeurs"][routeur]
    commandes = []
    for interface in dico_voisins.keys():
        commandes.extend(config_ripng(interface))
    commandes.extend(config_ripng("Loopback0"))
    return commandes

def test():
    """
    outdated mais a servi à tester les fonctions précédemments
    """
    with open("reseau_officiel.json") as fichier:
        reseau_officiel=json.load(fichier)
    print(rip_voisins("R3",reseau_officiel))

if __name__=="__main__":
    import json

    test()