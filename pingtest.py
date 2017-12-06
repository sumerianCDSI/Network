#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#Ping utilise une requête ICMP Request et attend une réponse Reply. L'envoi est répété pour des fins statistiques : déterminer le taux de paquets perdus et le délai moyen de réponse. 
#Si d'autres messages ICMP sont reçus de la part de routeurs intermédiaires (comme TTL exceeded, Fragmentation needed, administratively prohibited…), ils sont affichés à l'écran.
#Ce script explique le fonctionnement d'une enquête IP


import re
import random
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #Ignorer l'erreur de IPv6 lors l'utilisation de Scapy
from scapy.all import *
from scapy.all import *


##Définissons une fonction ping pour une seule requête
def ping_one(ip,id_icmp,id_seq):
    send_time = time.time()
    try:
        #On récupère la réponse par une requête scapy (Packet Ethernet) enquête de IP
        recev = sr1(IP(dst=ip,ttl=128)/ICMP(id=id_icmp,seq=id_seq),verbose = False)
        recev_time =time.time()
        ip_source = recev.getlayer(IP).src
        recev_seq = recev.getlayer(ICMP).seq
        pass_time = (recev_time - send_time)*1000
        recev_ttl = recev.getlayer(IP).ttl
        return ip_source, recev_seq, recev_ttl, pass_time
    except Exception as e:
        if re.match('.*NoneType.*',str(e)):
            return None

##Définissons une fonction ping pour 6 requêtes
def multi_ping(ip):
    id_icmp = random.randint(1,65535)
    for i in range(1,6):
        ping_list = ping_one(ip,id_icmp,i)
        if ping_list:
            print("From %s: icmp_seq=%s ttl=%d time= %3.2f ms"  % (ping_list[0],ping_list[1],ping_list[2],ping_list[3]))
        else:
            print('.',end='',flush= True)
        time.sleep(1)


if __name__ == '__main__':
    multi_ping(sys.argv[1])

