

import write_config as wc
import multiprocessing
import telnet

config_noeuds={}

def write_telnet_and_save(port,commande,routeur):
    config=telnet.configure_router_telnet("127.0.0.1",port,commande)
    wc.creer_fichier_config(routeur,config)

    pass

def handle_non_serializable(obj):
    # Retourne une valeur sérialisable pour les objets non sérialisables
    try:
        return str(obj)  # Convertit en chaîne
    except Exception:
        return None  # Ignore l'objet non sérialisable

def reinitialiser_routeur(routeur):
    port=config_noeuds[routeur]["json_gns3"].console
    print("réinitialisation de",routeur)
    telnet.reinitialise_router_telnet("127.0.0.1",port)
    

def config_routeur(routeur,graphe,config_noeuds,numas,process):
    protocole=graphe[numas]["protocole"] #récupérer le protocole ici
    router_id=config_noeuds[routeur]["router_id"]#récupérer le routeur_id ici
    #le graphe est le dico obtenu à partir du json
    commande=ad.genere_commandes_ip(config_noeuds,routeur)
    commande+=lb.generer_loopback_commandes(routeur,protocole,5,config_noeuds)
    #mettre bgp après ospf/rip (il faut avoir configuré le routage ipv6#)
    if protocole.lower()=="ospf":
        commande+=ospf.config_ospf(router_id,routeur,5,graphe,numas,1) 
    elif protocole.lower()=="rip":
        commande+=rip.config_rip_routeur(routeur,graphe,numas)
    else:
        print("protocole non reconnu")
        raise
    commande+=bgp.config_bgp_routeur(routeur,graphe,router_id,config_noeuds)
    commande+=bgp.config_iBGP(routeur,graphe,router_id,config_noeuds,numas)
    #commande+=loopback.generer_loopback_commandes(routeur,"ospf")

    
    port=config_noeuds[routeur]["json_gns3"].console

    p=multiprocessing.Process(target=write_telnet_and_save,args=(port,commande,routeur))
    p.start()
    process.append(p)
if __name__=="__main__":
    from gns3fy import Gns3Connector, Project

    import adresses as ad
    import BGP as bgp
    import router_id as id
    import RIP as rip
    import ospf
    import telnet
    import loopback as lb
    import json #on ne veut pas tout importer dans chaque process (ça prend beaucoup de temps)

    with open("gns/reseau_officiel.json") as fichier:
        graphe=json.load(fichier)

    GNS3_SERVER = "http://127.0.0.1:3080"
    PROJECT_NAME = input("quel est le nom de votre projet ? (sensible à la casse)")
    
    # Connexion au serveur GNS3
    connector = Gns3Connector(GNS3_SERVER)

    # Récupérer le projet par son nom
    project = Project(name=PROJECT_NAME, connector=connector)
    project.get()
    #question=input("voulez-vous réinitialiser les configurations avant d'appliquer les nouvelles ? (oui/non)")
    process=[]
    config_noeuds=ad.attribue_ip(graphe,config_noeuds)
    id.config_router_id(graphe,config_noeuds)

    lb.configure_looback_addresses(config_noeuds)
    telnet.recupérer_jsongns3_routeur(config_noeuds,project)
    with open("config_noeuds.json","w") as outfile:
        json.dump(config_noeuds,outfile,default=handle_non_serializable)
    # if question=="oui":
    #     for numas in graphe.keys():
    #         for routeur in graphe[numas]["routeurs"].keys():
    #             reinitialiser_routeur(routeur)
        
    #     pass #réinitialiser la config

    
    for numas in graphe.keys():
        for routeur in graphe[numas]["routeurs"].keys():
            config_routeur(routeur,graphe,config_noeuds,numas,process) #on configure tous les routeurs
    for p in process:
        p.join()



