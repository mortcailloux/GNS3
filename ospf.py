import json

def config_ospf(router_id, process_id, neighbor_list):
    """
    Args:
        str: l'id du routeur
        int: l'id du process
        list: la liste des voisins (rangée dans l'ordre des numéros d'interface)

    Returns:
        list: liste des commandes pour configurer OSPF sur les routeurs
    """
    commands = ["conf t"]

    # Generate the router OSPF configuration commands
    commands.append(f"ipv6 router ospf {process_id}")
    commands.append(f"router-id {router_id}")
    commands.append("exit")

    # Generate interface-specific OSPF commands for neighbor_list
    for i, neighbor in enumerate(neighbor_list):
        if i == 0:
            interface_name = "FastEthernet 0/0"
            commands.append(f"interface {interface_name}")
            commands.append(f"ipv6 ospf {process_id} area 0")
            commands.append("exit")
        else:
            interface_name = f"GigabitEthernet {i-1}/0"
            commands.append(f"interface {interface_name}")
            commands.append(f"ipv6 ospf {process_id} area 0")
            commands.append("exit")

    return commands




