#!/usr/bin/python3.5
# -*- coding=utf-8 -*-

#Lors d'une transmission de données informatiques, le maximum transmission unit (MTU) est la taille maximale d'un paquet pouvant être transmis en une seule fois (sans fragmentation) sur une interface.
#Le path MTU désigne la taille maximale entre une machine source et une machine destination. Il est égal au plus petit MTU des interfaces via lesquelles le paquet est transmis.
#Ce script peut déterminer le MTU d'une topologie de réseaux

import optparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #Ignorer l'erreur de IPv6 lors l'utilisation de Scapy
from scapy.all import *

def ping_df(dst,mtu):
    #La taille de la donnée= la taille du datagramme - la taille de l'entête IP (20) - la taille de l'entête ICMP (8)
    pyload = b'v'*(int(mtu) - 28)
    #On récupère l'information par une requête IP scapy
    ping_one_reply = sr1(IP(dst=dst,flags='DF')/ICMP()/pyload, timeout = 1, verbose=False)
    #(DF: don't fragment: quand DF=1, la fragmentation n'est pas autorisée. Un datagramme long qui doit être fragmenté et qui a un flag DF à 1 est dans une situation contradictoire, il sera détruit)
    try:
        if ping_one_reply.getlayer(ICMP).type == 3 and ping_one_reply.getlayer(ICMP).code == 4:
#ICMP type3 code4: fragmentation nécessaire mais interdite par le drapeau DF. 
            return 1, mtu
        elif ping_one_reply.getlayer(ICMP).type == 0 and ping_one_reply.getlayer(ICMP).code == 0:
#ICMP type 8 code 0: demande d'écho ou Echo request: Ce message demande le renvoi des informations envoyées avec la commandeping ou traceroute.
#ICMP type 0 code 0: réponse d'écho ou Echo reply: c'est la réponse au message de type 8.
            return 2, mtu
    except Exception as e:
        if re.match('.*NoneType.*',str(e)):
            return None


def discover_path_mtu(dst):
    mtu = 1500 #Par défaut, le mtu d'un routeur de cisco est 1500
    while True:
        Result = ping_df(dst,mtu)
        if Result == None:
            print('Destination Host: ' + dst + ' unreachable！')
            break
        elif Result[0] == 2:
            print('Destination Host Reachable, MTU: '+str(mtu))
            break
        elif Result[0] == 1:
            #Chqaue fragment doit être un mutiple de 8 sauf le dernier fragment
            mtu = mtu - 8
            print('Destination Hoste Reachable，reduce MTU！')
        time.sleep(1)


#Définissons des options
if __name__ == '__main__':
    #Example 
    parser = optparse.OptionParser('python3 path_mtu.py --ip [IP]')
    #Add une option "--ip" 
    parser.add_option('--ip', dest = 'ip', type = 'string', help = 'cible IP')
    (options, args) = parser.parse_args()
    ip = options.ip
    #Si la commande est sans option, on affiche l'example
    if ip == None:
        print(parser.usage)
    #On effectue la fonction et affiche le résultat 
    else:
        discover_path_mtu(ip)
