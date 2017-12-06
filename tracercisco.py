#!/usr/bin/python3.5
# -*- coding=utf-8 -*-

#traceroute (ou tracert sous Windows) est un programme utilitaire qui permet de suivre les chemins qu'un paquet de données (paquet IP) va prendre pour aller de la machine locale à une autre machine connectée au réseau IP.
#Ce script montre le mécanisme de "traceroute" pour les routeurs de cisco

import optparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #Ignorer l'erreur de IPv6 lors l'utilisation de Scapy
from scapy.all import *

def tracer(ip):
    for i in range(0,10):
        pkt = IP(dst=ip, ttl=i+1)/UDP(dport=33434+i,sport=50000+i) #le port UDP d'un routeur cisco est 33434 par default
        #On récupère l'information par une requête scapy 
        reply = sr1(pkt,verbose = False)
        if reply == None:
            break
        elif reply.type == 3 and reply.code == 3: #ICMP.type 3 code 3: le port inaccessible   
            print("%d hop: " % (i+1),reply.src)
            break
        elif reply.type == 11: #ICMP.type 11: Ce message est envoyé lorsque le temps de vie d'un datagramme ou le temps de réssemblage des parties d'un datagramme est dépassé. 
            print("%d hop: " % (i+1),reply.src)


#Définissons des options
if __name__ == "__main__":
    #Example 
    parser = optparse.OptionParser('python tracercisco.py --ip [cible IP]')
    #Add une option "--ip" 
    parser.add_option('--ip',dest= 'ip', type='string', help= 'cible IP')
    (options,args) = parser.parse_args()
    ip = options.ip
    #Si la commande est sans option, on affiche l'example
    if ip == None:
        print(parser.usage)
    else:
        #On effectue la fonction et affiche le résultat
        tracer(ip)
