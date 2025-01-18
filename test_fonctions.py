import adresses as ad
import BGP as bgp
import json
import router_id as id
import RIP as rip
import ospf
import telnet
import loopback
import write_config as wc
config_noeux={}
with open("gns/reseau_officiel.json") as fichier:
    graphe=json.load(fichier)
"""alloue les ip en fonction du graphe"""
#le graphe est le dico obtenu à partir du json
config_noeux=ad.attribue_ip(graphe,config_noeux)
print(config_noeux)
id.config_router_id(graphe,config_noeux)
commande=ad.genere_commandes_ip(config_noeux,"R1")
#commande+=bgp.config_bgp_routeur("R1",graphe,config_noeux["R1"]["router_id"],config_noeux)
#commande+=rip.config_rip_routeur("R1",graphe)
#commande+=ospf.config_ospf("1.1.1.1","R1",5,graphe,str(bgp.get_as_for_router("R1",graphe)),1) #attention pour accéder à la clé 

#commande+=loopback.generer_loopback_commandes("R1","ospf")
print(commande)

telnet.recupérer_jsongns3_routeur(config_noeux)
port=config_noeux["R1"]["json_gns3"].console
print(port)
config=telnet.configure_router_telnet("127.0.0.1",port,commande)
print(config)
wc.creer_fichier_config("R1",config)

