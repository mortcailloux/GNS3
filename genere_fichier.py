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
    for i in range(nb_as):
        dic[i]={}
        protocole=demande_protocole()
        dic[i]["protocole"]=protocole
        nb_routeurs=demande_nb_routeurs()
        switch_present=demande_presence_switch()
        if switch_present:
            nb_switch=randint(1,5) 
            for i in range(nb_switch):
                
                pass #à compléter