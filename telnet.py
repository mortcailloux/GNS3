import telnetlib
import time
from gns3fy import Gns3Connector, Project

# Configuration du serveur GNS3
GNS3_SERVER = "http://127.0.0.1:3080"
PROJECT_NAME = input("quel est le nom de votre projet ? (sensible à la casse)")  # Remplacez par le nom de votre projet



def configure_router_telnet(ip, port, commands):
    """Execute les commandes fournies sur le routeur à l'aide de telnet"""
    try:
        tn = telnetlib.Telnet(ip, port)
        tn.read_until(b"Router>", timeout=5)
        tn.write(b"enable\r\n")
        tn.read_until(b"Router#", timeout=2)
        
        # Séparer les commandes correctement
        
        
        for command in commands:
            tn.write(command.encode('ascii') + b"\r\n")
            # Attendre la réponse du routeur après chaque commande
            output = tn.read_until(b"#", timeout=2).decode('ascii')
            print(output)
            time.sleep(1)  # Augmenter le délai entre les commandes
            
        tn.write(b"exit\r\n")
        tn.close()
        
    except Exception as e:
        print(f"Erreur lors de la configuration : {e}")
# Exemple d'utilisation
  # Le port Telnet vient de l'API GNS3
#le port est ensuite stocké dans config_noeud, accès: noeud_config["nom_noeud"]["json_gns3"]["console"]

# Connexion au serveur GNS3
connector = Gns3Connector(GNS3_SERVER)

# Récupérer le projet par son nom
project = Project(name=PROJECT_NAME, connector=connector)
project.get()

def recupérer_jsongns3_routeur(project_gns,config_noeuds):
    """mets le json de gns3 dans la config des noeuds"""
    for routeur in project_gns.nodes:
        nom=routeur.name #normalement le nom est identique à un routeurs que l'on a déjà renseigné dans le dictionnaire
        config_noeuds[nom]["json_gns3"]=routeur

def trouve_port_telnet_routeur(routeur,project_gns3):
    """sert à trouver le port de connexion à telnet"""
    for node in project_gns3.nodes:
        if node.name==routeur:
            print(node.__dict__)
            return node.console

"""
tests
port=trouve_port_telnet_routeur("R5",project)
print(port)
configure_router_telnet("127.0.0.1",port,["configure terminal","interface FastEthernet0/0","ipv6 enable","ipv6 address 2001:156:45::/64","no shutdown", "exit", "exit"])
"""