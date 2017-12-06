#!/usr/bin/python3.5
# -*- coding=utf-8 -*-

#Ce script permet de trouver l'adresse MAC d'une périphérique réseau (Uniquement pour l'OS linux)

import os
import re
import optparse

#Définissons une fonction avec un seul paramètre (le nom de la carte réseau)
def get_mac_address(iface):
    #On effectue la commande linux ifconfig iface et enregistre dans un objet "data"
    data = os.popen("ifconfig " + iface).read()
    #On scinde l'information et met tous les morceaux dans une list "words"
    words = data.split()
    found = 0
    location = 0
    index = 0
    #On cherche l'adresse MAC dans la list "words" en utilisant l'expression régulière "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
    for x in words:
        if re.match('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', x):
            found = 1
            index = location
            break
        else:
            location = location + 1
    if found == 1:
        mac = words[index]
    else:
        mac = 'Mac not found'
    return mac

#Définissons des options
if __name__ == "__main__":
    #Example 
    parser = optparse.OptionParser('python3 GET_MAC.py -i interface')
    parser.add_option('-i', dest = 'ifname', type = 'string', help = 'interface')
    (options, args) = parser.parse_args()
    ifname = options.ifname
    #Si la commande est sans option, on affiche l'example
    if ifname == None:
        print(parser.usage)
    #On effectue la fonction et affiche le résultat    
    else:
        print(get_mac_address(ifname))


