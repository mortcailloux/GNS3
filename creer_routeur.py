import requests
from random import randint
GNS3_SERVER = "http://127.0.0.1:3080"
PROJECT_ID = "votre_project_id"  # Remplacez par l'ID de votre projet GNS3

def create_router(name, template_id, x=0, y=0):
    """
    Crée un routeur dans le projet GNS3 en utilisant l'API REST.
    """
    url = f"{GNS3_SERVER}/v2/projects/{PROJECT_ID}/nodes"
    payload = {
        "name": name,
        "template_id": template_id,  # ID du template (par ex. IOSv, etc.)
        "x": x,
        "y": y
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print(f"Routeur {name} créé avec succès.")
        return response.json()
    else:
        print(f"Erreur lors de la création du routeur {name}: {response.text}")
        return None

# Exemple d'utilisation
router1 = create_router("Router1", "iosv-template-id", x=100, y=100)
router2 = create_router("Router2", "iosv-template-id", x=300, y=100)

def coordonnees_routeur_aleatories():
    """renvoie un couple x,y aléatoire"""
    return randint(1,1000),randint(1,1000)

