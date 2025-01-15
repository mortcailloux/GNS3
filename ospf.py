import json

def config_ospf(router_id, process_id, neighbor_list, cost=0):
    """
    Args:
        str: l'id du routeur
        int: l'id du process
        list: la liste des voisins (rangée dans l'ordre des numéros d'interface)
        int: la métrique du lien (0 si valeur pas défaut)

    Returns:
        list: liste des commandes pour configurer OSPF sur les routeurs
    """
    commands = ["conf t"]

    # Generate the router OSPF configuration commands
    commands.append(f"ipv6 router ospf {process_id}")
    commands.append(f"router-id {router_id}")
    commands.append("exit")

    # Generate interface-specific OSPF commands for neighbor_list
    for i in range(len(neighbor_list)):
        if i == 0:
            interface_name = "FastEthernet 0/0"
            commands.append(f"interface {interface_name}")
            commands.append(f"ipv6 ospf {process_id} area 0")
            if cost:
                commands.append(f"ipv6 ospf cost {cost}")
            commands.append("exit")
        else:
            interface_name = f"GigabitEthernet {i-1}/0"
            commands.append(f"interface {interface_name}")
            commands.append(f"ipv6 ospf {process_id} area 0")
            if cost:
                commands.append(f"ipv6 ospf cost {cost}")
            commands.append("exit")

    return commands

