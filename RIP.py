def config_ripng(routeur, voisins):
	"""
	configuration de RIP sur routeur(string) relié à voisins(liste)
	à partir du fichier JSON reseau_officiel.json
	"""
	commandes = ["config term","ipv6 unicast-routing","ipv6 router rip ripng",
			  "redistribute connected"]
	for i in range(len(voisins)):
		if i ==0: #pour aller d'abord sur FastEthernet
			interface = "FastEthernet0/0" 
		else:
			interface = f"GigabitEthernet{i}/0"
		commandes.append(f"interface {interface}")
		commandes.append("ipv6 rip ripng enable")
		commandes.append("exit") # afin de sortir de l'interface du routeur
	commandes.append("exit")#pour sortir de config terminal
	return commandes
