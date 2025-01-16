import adresses as ad
import BGP as bgp
import json
import router_id as id
import RIP as rip
import ospf
config_noeux={}
with open("gns/reseau_officiel.json") as fichier:
    graphe=json.load(fichier)
"""alloue les ip en fonction du graphe"""
#le graphe est le dico obtenu à partir du json
config_noeux=ad.attribue_ip(graphe,config_noeux)
print(config_noeux)
id.config_router_id(graphe,config_noeux)
commande=bgp.config_bgp_routeur("R1",graphe,config_noeux["R1"]["router_id"],config_noeux)
commande+=rip.config_rip_routeur("R1",graphe)
print(commande)
commande+=ospf.config_ospf("1.1.1.1","R1",5,graphe,str(bgp.get_as_for_router("R1",graphe)),1)
