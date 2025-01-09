import datetime
import json
from random import randint

def demande_protocole():
    text=""
    while text!="OSPF" and text!="RIP":
        text=input("Quel protocole cet as utilise-t-il ? (OSPF ou RIP)")
        text=text.upper().strip()
    return text
def demande_nb_routeurs():
    entier=-1
    while entier<=0 :
        try:
            entier=int(input("entrez le nombre de routeurs présents dans cet as"))
        except:
            return demande_nb_routeurs()
    return entier
def demande_presence_switch():
    text=""
    while text!="oui" and text!="non":
        text=input("Voulez vous utiliser un ou plusieurs switchs ? (vous ne choisissez pas le nombre ni les connexions)")
        text=text.lower().strip()
    return text=="oui"



def genere_dic(nb_as):
    dic={}
    for i in range(1,nb_as+1):
        dic[i]={}
        aretes=set()
        print("nous nous occupons de l'AS {i+1}")

        protocole=demande_protocole()
        dic[i]["protocole"]=protocole
        dic[i]["routeurs"]={}
        dic[i]["switches"]={}
        nb_routeurs=demande_nb_routeurs()
        switch_present=demande_presence_switch()
        if switch_present:
            nb_switch=randint(1,5) 
            for j in range(nb_switch):
                switch=f"switch{j+1}"
                
                deja_co=set() #on retient les routeurs que l'on a déjà connecté au switch
                dic[i]["switches"][switch]=[]
                for k in range(randint(2,19)): #max 20 connexion sur un switch, min 2 sinon aucun intérêt d'avoir un switch
                    routeur=f"noeud{randint(1,nb_routeurs)}"
                    if routeur not in deja_co:
                        deja_co.add(routeur)
                        dic[i]["switches"][f"switch{j+1}"].append(routeur)
                        if routeur not in dic[i]["routeurs"].keys():
                            dic[i]["routeurs"][routeur]=[]
                        dic[i]["routeurs"][routeur].append(switch)
            
        for j in range(nb_routeurs):
            routeur=f"noeud{j+1}"
                
            if routeur not in dic[i]["routeurs"].keys():
                dic[i]["routeurs"][routeur]=[]
                
                #chaque routeur ne peut être connecté qu'à un seul autre routeur (lui aussi connecté au premier)
            nb_alea=randint(1,nb_routeurs)
            while nb_alea==j+1:
                nb_alea=randint(1,nb_routeurs) #on ne veut pas être connecté à soi-même
            routeur2=f"noeud{nb_alea}"
            if routeur2 not in dic[i]["routeurs"].keys():
                dic[i]["routeurs"][routeur2]=[]
            if (routeur,routeur2) not in aretes and (routeur2,routeur) not in aretes: # si on n'a pas déjà fait l'arête
                dic[i]["routeurs"][routeur].append(routeur2)
                dic[i]["routeurs"][routeur2].append(routeur) 

    return dic


def genere_json():
    nb_as=int(input("Combien voulez-vous d'AS (attention après il faut redonner le nombre de routeur et de switch à chaque AS)"))
    dic=genere_dic(nb_as)
    with open ("gns/exemple.json","w") as fichier:
        json.dump(dic,fichier)
                

genere_json()