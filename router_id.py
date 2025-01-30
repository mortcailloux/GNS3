"""
module qui génère l'id X.X.X.X pour les routeurs où X est le numéro du routeur (255 routeurs max)
"""

import json

def config_router_id(graphe,config_noeud):
	"""
	génère et configure un id pour tous les routeurs et le stock dans config_noeud
	graphe: graphe du réseau (liste d'adjacence)
	config_noeud: dictionnaire de config
	"""
	for AS in graphe.keys():
		for noeud in (graphe[AS]["routeurs"]).keys():
			num_id = noeud[1::] # recuperation du numero_id (on supprime le R)
			int(num_id)
			router_iden = f"{num_id}.{num_id}.{num_id}.{num_id}"
			if noeud not in config_noeud.keys():
				config_noeud[noeud]={}
			
			config_noeud[noeud]["router_id"] = router_iden
	return config_noeud


def test():
	"""
	teste les fonctions du fichier avant intégration dans gns.py
	"""
	with open("exemple_desc_reseau.json") as fichier:
		graphe=json.load(fichier)
	config_noeud={}
	print(config_router_id(graphe,config_noeud))
if __name__=="__main__":
	test()
