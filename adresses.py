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
            for interface,connexion in graphe[ass]["routeurs"][routeur].items():
                connexion=connexion[0] #on n'a pas besoin d'utiliser le coût
                if (connexion,routeur) not in reseaux.keys() and (routeur,connexion) not in reseaux.keys():
                    if "switch" in connexion:
                        nbrouteur= len(graphe[ass]["switches"][connexion])+1
                        ips=genere_ip_reseau(num_reseau,nbrouteur,ass)
                        if routeur not in config_noeux.keys():
                            config_noeux[routeur]={}
                            config_noeux[routeur]["ip_et_co"]={}
                            
                            config_noeux[routeur]["protocole"]=graphe[ass]["protocole"]
                        config_noeux[routeur]["ip_et_co"][connexion]=[interface,ips.pop()] #l'ip de l'interface du routeur routeur vers le routeur connexion est la dernère de la liste
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
                        if "ip_et_co" not in config_noeux[routeur]:
                            config_noeux[routeur]["ip_et_co"]={}
                        
                        config_noeux[routeur]["ip_et_co"][connexion]=[interface,ips.pop()] #l'ip de l'interface du routeur routeur vers le routeur connexion est la dernère de la liste
                        reseaux[(connexion,routeur)]=[num_reseau,ips]
                        reseaux[(routeur,connexion)]=[num_reseau,ips]
                    num_reseau+=1
                else:
                    if routeur not in config_noeux.keys():
                            config_noeux[routeur]={}
                            config_noeux[routeur]["ip_et_co"]={}
                    a,ips=reseaux[(routeur,connexion)] #patch duplication d'IP
                    config_noeux[routeur]["ip_et_co"][connexion]=[interface,ips.pop()]
                    num_reseau+=1
    return config_noeux




def main():
    config_noeux={}
    with open("gns/reseau_officiel.json") as fichier:
        graphe=json.load(fichier)
    """alloue les ip en fonction du graphe"""
    #le graphe est le dico obtenu à partir du json
    config_noeux=attribue_ip(graphe,config_noeux)
    print(config_noeux)

def genere_commandes_ip(config_noeuds,noeud):
    """génère les commandes pour configurer les addresses ip"""
    commande=["configure terminal"]
    for interface,ip in config_noeuds[noeud]["ip_et_co"].values():
        commande.append(f"interface {interface}")
        commande.append('ipv6 enable')
        commande.append(f"ipv6 address {ip}")
        commande.append("no shutdown")
        commande.append("exit")

    commande.append("exit")
    return commande
    


if __name__=="__main__":

    main()

