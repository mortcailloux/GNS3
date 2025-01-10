import json

def config_router_id(graphe,config_noeud):
	
	for AS in graphe.keys():
		for noeud in (graphe[AS]["routeurs"]).keys():
			num_id = noeud[-1] # recuperation du numero_id
			int(num_id)
			router_iden = f"{num_id}.{num_id}.{num_id}.{num_id}"
			if noeud not in config_noeud.keys():
				config_noeud[noeud]={}
			
			config_noeud[noeud]["router_id"] = router_iden
	return config_noeud


def test():
	with open("exemple_desc_reseau.json") as fichier:
		graphe=json.load(fichier)
	config_noeud={}
	print(config_router_id(graphe,config_noeud))

test()
