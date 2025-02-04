# Projet Configuration auto d'un réseau sur GNS3

Le Programme principal ([gns.py](https://github.com/mortcailloux/GNS3/blob/main/gns.py)) permet de configurer automatiquement tous les routeurs suivant le fichier d'intention [normal](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel.json) ou avec [policies](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel_policies.json). 

## structure du projet:
Le projet est structuré en plusieurs modules dont la description est donnée ci-dessous:
- [BGP.py](https://github.com/mortcailloux/GNS3/blob/main/BGP.py): génère les commandes relatives à BGP pour la configuration des routeurs.
- [RIP.py](https://github.com/mortcailloux/GNS3/blob/main/RIP.py): génère les commandes relatives à RIP pour la configuration des routeurs.
- [adresses.py](https://github.com/mortcailloux/GNS3/blob/main/RIP.py): génère dynamiquement les adresses ip des interfaces puis génère les commandes de configuration relatives aux IP et aux interfaces pour la configuration des routeurs.
- [exemple_desc_reseau.json](https://github.com/mortcailloux/GNS3/blob/main/exemple_desc_reseau.json): premiere ébauche de ce à quoi ressemblerait notre fichier d'intention, incomplet
- [gns.py](https://github.com/mortcailloux/GNS3/blob/main/gns.py): permet de configurer tous les routeurs en combinant les modules. Lance telnet et l'écriture de config sur des process indépendants afin de pouvoir continuer à générer les commandes en parallèle.
- [loopback.py](https://github.com/mortcailloux/GNS3/blob/main/loopback.py): permet de configurer les interfaces de loopback en générant les commandes correspondantes.
- [ospf.py](https://github.com/mortcailloux/GNS3/blob/main/ospf.py): permet de générer les commandes nécessaires pour configurer OSPF sur les routeurs concernés.
- [reseau_officiel.json](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel.json): fichier d'intention décrivant le réseau correspondant à la démo sans les policies.
- [reseau_officiel_policies.json](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel_policies.json): fichier d'intention décrivant le réseau pour la démo avec les policies (on a rajouté des routeurs et des AS pour pouvoir montrer que cela fonctionne bien)
- [routeur_id.py](https://github.com/mortcailloux/GNS3/blob/main/router_id.py): génère les router_id qui seront utilisés par BGP.py.
- [structure_config_noeud.json](https://github.com/mortcailloux/GNS3/blob/main/structure_config_noeud.json): fichier qui décrit à quoi ressemble notre dictionnaire de configuration des noeuds (qui est généré au cours du programme). Pratique pour s'y retrouver dans le code.
- [telnet.py](https://github.com/mortcailloux/GNS3/blob/main/telnet.py): fichier qui contient les fonctions qui permettent d'écrire les commandes dans la console du routeur.
- [test_fonctions.py](https://github.com/mortcailloux/GNS3/blob/main/test_fonctions.py): test des fonctions individuellement puis collectivement pour débugger (n'est plus à jour)/
- [write_config.py](https://github.com/mortcailloux/GNS3/blob/main/write_config.py): permet d'écrire la config dans un fichier et de formatter le nom du fichier conformément à gns3.
- creer_routeur.py et genere_fichier.py: servaient à créer intégralement le réseau, mais au final ce n'est pas ce qu'il fallait faire



## Execution du programme:
Il suffit de lancer le script [gns.py](https://github.com/mortcailloux/GNS3/blob/main/gns.py) en ayant gns3 de lancé, rentrez ensuite le nom de votre projet et le programme se charge du reste !

## librairies utilisées:
Le programme utilise telnetlib, gns3fy, multiprocessing et json. Il vous faudra installer la librairie correspondante s'il vous la manque.

## structure du fichier d'intention:
la première clé est le numéro de l'AS, ensuite on a le choix entre protocole (qui sert à récupérer le protocole utilisé dans l'as), routeurs (qui sert à savoir quels routeurs sont présents dans l'as) et relation qui permet d'établir les relations clients/peer/provider de cet as vers les autres as.
Dans les routeurs, on retrouve un dictionnaire à chaque routeur dans lequel on retrouve les interfaces associés aux routeurs auxquelles elles sont connectées et le coût OSPF associé (ignoré dans RIP, on peut le modifier pour OSPF)