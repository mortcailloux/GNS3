import adresses as ad
import BGP as bgp
import json
import router_id as id
import RIP as rip
import ospf
import telnet
import loopback as lb
import write_config as wc
config_noeuds={}
with open("gns/reseau_officiel.json") as fichier:
    graphe=json.load(fichier)

def reinitialiser_routeur(routeur):
    port=config_noeuds[routeur]["json_gns3"].console
    print("réinitialisation de",routeur)
    telnet.reinitialise_router_telnet("127.0.0.1",port)
    

def config_routeur(routeur,graphe,config_noeuds,numas):
    protocole=graphe[numas]["protocole"] #récupérer le protocole ici
    router_id=config_noeuds[routeur]["router_id"]#récupérer le routeur_id ici
    #le graphe est le dico obtenu à partir du json
    commande=ad.genere_commandes_ip(config_noeuds,routeur)
    commande+=lb.generer_loopback_commandes(routeur,protocole,5,config_noeuds)
    #mettre bgp après ospf/rip (il faut avoir configuré le routage ipv6#)
    if protocole.lower()=="ospf":
        commande+=ospf.config_ospf(router_id,routeur,5,graphe,numas,1) 
    elif protocole.lower()=="rip":
        commande+=rip.config_rip_routeur(routeur,graphe)
    else:
        print("protocole non reconnu")
        raise
    commande+=bgp.config_bgp_routeur(routeur,graphe,router_id,config_noeuds)
    commande+=bgp.config_iBGP(routeur,graphe,router_id,config_noeuds,numas)
    #commande+=loopback.generer_loopback_commandes(routeur,"ospf")

    
    port=config_noeuds[routeur]["json_gns3"].console
    config=telnet.configure_router_telnet("127.0.0.1",port,commande)
    wc.creer_fichier_config(routeur,config)
if __name__=="__main__":
    #question=input("voulez-vous réinitialiser les configurations avant d'appliquer les nouvelles ? (oui/non)")
    
    config_noeuds=ad.attribue_ip(graphe,config_noeuds)
    id.config_router_id(graphe,config_noeuds)

    lb.configure_looback_addresses(config_noeuds)
    telnet.recupérer_jsongns3_routeur(config_noeuds)
    
    # if question=="oui":
    #     for numas in graphe.keys():
    #         for routeur in graphe[numas]["routeurs"].keys():
    #             reinitialiser_routeur(routeur)
        
    #     pass #réinitialiser la config

    
    for numas in graphe.keys():
        for routeur in graphe[numas]["routeurs"].keys():
            config_routeur(routeur,graphe,config_noeuds,numas) #on configure tous les routeurs




