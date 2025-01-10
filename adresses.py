import json



def genere_ip_reseau(numreseau,nbrouteur,numass=168):
    return [f"2001:{numass}:{numreseau}::{i+1}/64" for i in range(nbrouteur)]

def attribue_ip(graphe,config_noeux):
    """entrée: le graphe, la config des noeuds (le graphe avec les IP et les routeurs id)
    type de sortie: dict{dict{dict}}
    le premier dictionnaire contient les noms des routeurs (uniques), le 2e contient les configurations diverses (protocole de routage, les ips et les arêtes connectées, le routeur ID si on est en OSPF)
    """
    reseaux={}
    num_reseau=1
    for ass in graphe.keys():
        for routeur in graphe[ass]["routeurs"]:
            
            for connexion in graphe[ass]["routeurs"][routeur]:
                if (connexion,routeur) not in reseaux.keys():
                    if "switch" in connexion:
                        nbrouteur= len(graphe[ass]["switches"][connexion])+1
                        ips=genere_ip_reseau(num_reseau,nbrouteur,ass)
                        if routeur not in config_noeux.keys():
                            config_noeux[routeur]={}
                            config_noeux[routeur]["ip_et_co"]={}
                            
                            config_noeux[routeur]["protocole"]=graphe[ass]["protocole"]
                        config_noeux[routeur]["ip_et_co"][connexion]=ips.pop() #l'ip de l'interface du routeur routeur vers le routeur connexion est la dernère de la liste
                        #s'il y a un switch il y a plus de deux routeurs sur le réseau
                        for lien in graphe[ass]["switches"]:
                            reseaux[(connexion,routeur)]=[num_reseau,ips]
                            reseaux[(routeur,connexion)]=[num_reseau,ips]

                    else:
                        nbrouteur=2
                        ips=genere_ip_reseau(num_reseau,nbrouteur,ass)
                        #s'il n'y a pas de switch il n'y a que deux routeurs sur le reseau
                        if routeur not in config_noeux.keys():
                            config_noeux[routeur]={}
                            config_noeux[routeur]["ip_et_co"]={}
                        config_noeux[routeur]["ip_et_co"][connexion]=ips.pop() #l'ip de l'interface du routeur routeur vers le routeur connexion est la dernère de la liste
                        reseaux[(connexion,routeur)]=[num_reseau,ips]
                        reseaux[(routeur,connexion)]=[num_reseau,ips]
                    num_reseau+=1
                else:
                    if routeur not in config_noeux.keys():
                            config_noeux[routeur]={}
                    num_reseau,ips=reseaux[(routeur,connexion)]
                    config_noeux[routeur][connexion]=ips.pop()
    return config_noeux




def main():
    config_noeux={}
    with open("gns/exemple_desc_reseau.json") as fichier:
        graphe=json.load(fichier)
    """alloue les ip en fonction du graphe"""
    #le graphe est le dico obtenu à partir du json
    config_noeux=attribue_ip(graphe,config_noeux)
    print(config_noeux)
main()

