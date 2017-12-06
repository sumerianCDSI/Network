#!/usr/bin/python3.5
# -*- coding=utf-8 -*-

#Ce script permet de trouver l'adresse IP d'une périphrique réseau (Uniquement pour l'OS linux)

import socket
import fcntl
import struct
import optparse

#Définissons une fonction avec un seul paramètre (le nom de la carte réseau)
def get_ip_address(ifname):
	#Créons un socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Retouner l'adresse IP dans le résultat donné par la commande ifconfig ifname
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', (ifname[:15]).encode()))[20:24])


#Définissons des options
if __name__ == '__main__':
	#Example 
    parser = optparse.OptionParser('python3 GET_IP.py -i interface')
    #Add une option "-i" 
    parser.add_option('-i', dest = 'ifname', type = 'string', help = 'network interface')
    (option,args) = parser.parse_args()
    ifname = option.ifname
    #Si la commande est sans option, on affiche l'example
    if ifname == None:
        print(parser.usage)
    else:
        try:
        	#On effectue la fonction et affiche le résultat
            print(get_ip_address(ifname))
        except:
            print("Error")
