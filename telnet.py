import telnetlib
import time

def configure_router_telnet(ip, port, commands): #l'IP est l'IP de la machine sur laquelle on se connecte (ici on se connecte au gns local)
    """execute les commandes fournies sur le routeur à l'aide de telnet"""
    try:
        tn = telnetlib.Telnet(ip, port)
        tn.read_until(b"Router>", timeout=5)
        tn.write(b"enable\n")
        time.sleep(1)
        tn.write(b"configure terminal\n")
        time.sleep(1)
        for command in commands:
            tn.write(command.encode('ascii') + b"\n")
            time.sleep(0.5)
        tn.write(b"end\n")
        tn.write(b"exit\n")
        print(tn.read_all().decode('ascii'))
    except Exception as e:
        print(f"Erreur lors de la configuration : {e}")

# Exemple d'utilisation
commands = [
    "interface GigabitEthernet0/0",
    "ip address 192.168.1.1 255.255.255.0",
    "no shutdown"
]
configure_router_telnet("127.0.0.1", 5000, commands)  # Le port Telnet vient de l'API GNS3
#le port est ensuite stocké dans config_noeud, accès: noeud_config["nom_noeud"]["json_gns3"]["console"]
