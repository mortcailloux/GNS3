def clean_control_chars(text: str) -> str:
    """
    Nettoie les caractères de contrôle et les espaces superflus
    """
    #là pour le coup j'ai demandé à l'IA pour savoir ce qu'était les B5 en rouge sur vscode dans le fichier de config 
    import re
    # Supprime les caractères de contrôle tout en gardant les sauts de ligne normaux
    cleaned = re.sub(r'[\x00-\x09\x0B-\x1F\x7F-\xFF]', '', text)
    # Supprime les espaces multiples
    cleaned = re.sub(r' +', ' ', cleaned)
    # Supprime les lignes vides multiples
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    return cleaned

def format_cisco_config(input_text: str) -> str:
    """
    Formate une configuration Cisco à partir d'une sortie telnet
    """
    # Nettoie d'abord les caractères de contrôle
    input_text = clean_control_chars(input_text)

    # Divise le texte en lignes
    lines = input_text.split('\r\n') if '\r\n' in input_text else input_text.split('\n') #on split avec \r\n s'il y en a sinon avec \n
    #split crée une liste en séparant le string au caractère spécifié
    # Liste pour stocker les lignes formatées
    formatted_lines = []
    
    # Flag pour le contrôle du formatage
    previous_empty = False
    config_started = False
    fin=False
    for line in lines:
        # Détecte le début de la configuration réelle
        if 'version 15.2' in line:
            config_started = True
        if fin:
            continue
        if "login" in line:
            fin=True
        #on supprime les lignes présentes qui sont restés dans la sortie telnet et dont on n'a pas besoin
        if not config_started:
            continue
            
        # Ignore les lignes de début/fin de configuration
        if any(x in line for x in ['Building configuration', 'Current configuration', 'Last configuration', 
                                 'boot-start-marker', 'boot-end-marker', 'end']):
            continue
            
        # Supprime les espaces en début et fin de ligne
        line = line.strip()
        
        # Ignore les lignes vides consécutives (ça n'en ignore qu'une sur 2 mais ce n'est pas grave)
        if not line:
            if not previous_empty:
                formatted_lines.append('')
                previous_empty = True
            continue
        else:
            previous_empty = False
            
        # Ajoute un commentaire pour les interfaces
        if line.startswith('interface'):
            formatted_lines.append(f'\n! {line}')
        
        # Supprime les séries de points d'exclamation
        if line == '!' and formatted_lines and formatted_lines[-1] == '!':
            continue
            
        # Ajoute la ligne à la sortie
        formatted_lines.append(line)
    # Trouve l'index de la dernière ligne de configuration significative
    last_config_index = len(formatted_lines)
    for i in range(len(formatted_lines) - 1, -1, -1):
        if formatted_lines[i] and not formatted_lines[i].startswith('!'):
            last_config_index = i + 1
            break
            
    # Garde seulement les lignes de configuration
    formatted_lines = formatted_lines[:last_config_index]
    
    # Nettoie le début et la fin du fichier des lignes vides et points d'exclamation
    while formatted_lines and (not formatted_lines[0] or formatted_lines[0] == '!'):
        formatted_lines.pop(0)
    while formatted_lines and (not formatted_lines[-1] or formatted_lines[-1] == '!'):
        formatted_lines.pop()
    # Retourne la configuration formatée
    
    return '\n'.join(formatted_lines)  

def write_config(nom_routeur:str,config:str)->None:
    """
    écrit la config dans un fichier connaissant la config formattée et le nom du routeur
    """
    numero=nom_routeur[1::]
    
    with open(f"i{numero}_startup-config.cfg", "w") as fichier:
        fichier.write(config)


def creer_fichier_config(nom_routeur:str,config:str):
    """
    crée le fichier de config (combine les fonctions) sachant le nom du routeur et la config issue de telnet

    """
    config=format_cisco_config(config)
    write_config(nom_routeur,config)

