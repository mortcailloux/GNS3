import telnetlib
import time

def reinitialise_router_telnet(ip,port):
    try:
        tn = telnetlib.Telnet(ip, port)
        tn.write(b"\r\n")
        tn.read_until(b"Router>", timeout=5)
        tn.write(b"\r\n")

        tn.write(b"enable\r\n")
        tn.read_until(b"Router#", timeout=2)
        tn.write(b"\r\n")

        tn.write(b"erase startup-config\r\n")
        tn.read_until(b"Are you sure?", timeout=2)  # Si un message de confirmation apparaît
        tn.write(b"\r\n")
        tn.read_until(b"#", timeout=5)

        tn.write(b"reload\r\n")
        tn.read_until(b"Proceed with reload?", timeout=2)
        tn.write(b"\r\n")
        tn.read_until(b"#", timeout=5)
    except Exception as e:
        print(f"Erreur lors de la configuration : {e}")

def configure_router_telnet(ip, port, commands):
    """Execute les commandes fournies sur le routeur à l'aide de telnet"""
    try:
        tn = telnetlib.Telnet(ip, port)
        tn.write(b"\r\n")
        tn.read_until(b"Router>", timeout=5)
        tn.write(b"\r\n")

        tn.write(b"enable\r\n")
        tn.read_until(b"Router#", timeout=2)
        tn.write(b"\r\n")
        
        
        # Séparer les commandes correctement
        
        
        for command in commands:
            tn.write(command.encode('ascii') + b"\r\n")
            # Attendre la réponse du routeur après chaque commande
            output = tn.read_until(b"#", timeout=2).decode('ascii')
            print(output)
              # Augmenter le délai entre les commandes
        
        tn.write(b"write\r\n")
        
        tn.write(b"\r\n")
        tn.write(b"\r\n")
        tn.write(b"show running-config\r\n")
        output=""
        while True:
            # Lire une partie de la sortie
            chunk = tn.read_until(b"--More--", timeout=10).decode('ascii')
            output += chunk.replace("--More--", "")
            
            # Vérifier si la sortie est terminée
            if "--More--" not in chunk:
                break
            
            # Envoyer un espace pour continuer
            tn.write(b" ")
        
        tn.write(b"exit\r\n")
        tn.write(b"\r\n")

        tn.close()
        print("sauvegarde de la configuration")
        return output
        
    except Exception as e:
        print(f"Erreur lors de la configuration : {e}")
# Exemple d'utilisation
  # Le port Telnet vient de l'API GNS3
#le port est ensuite stocké dans config_noeud, accès: noeud_config["nom_noeud"]["json_gns3"]["console"]



def recupérer_jsongns3_routeur(config_noeuds, project_gns):
    """mets le json de gns3 dans la config des noeuds"""
    for routeur in project_gns.nodes:
        nom=routeur.name #normalement le nom est identique à un routeurs que l'on a déjà renseigné dans le dictionnaire
        if "PC" not in nom and "Switch" not in nom:
            config_noeuds[nom]["json_gns3"]=routeur

def trouve_port_telnet_routeur(routeur,project_gns3):
    """sert à trouver le port de connexion à telnet"""
    for node in project_gns3.nodes:
        if node.name==routeur:
            print(node.__dict__)
            return node.console

if __name__=="__main__":
    from gns3fy import Gns3Connector, Project

    # Configuration du serveur GNS3
    GNS3_SERVER = "http://127.0.0.1:3080"
    PROJECT_NAME = input("quel est le nom de votre projet ? (sensible à la casse)")  # Remplacez par le nom de votre projet
    
    # Connexion au serveur GNS3
    connector = Gns3Connector(GNS3_SERVER)

    # Récupérer le projet par son nom
    project = Project(name=PROJECT_NAME, connector=connector)
    project.get()
    #tests
    port=trouve_port_telnet_routeur("R5",project)
    print(port)
    configure_router_telnet("127.0.0.1",port,["configure terminal","interface FastEthernet0/0","ipv6 enable","ipv6 address 2001:156:45::/64","no shutdown", "exit", "exit"])
    