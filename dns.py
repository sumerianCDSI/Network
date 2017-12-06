#!/usr/bin/python3.5
# -*- coding=utf-8 -*-

#Ce script permet de simuler une enquête de DNS

import optparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #Ignorer l'erreur de IPv6 lors l'utilisation de Scapy
from scapy.all import *


#Définissons une fonction avec un seul paramètre (le nom de domaine de la machine)
def dns_query(domain_name):
	#On récupère l'information de la DNS par une requête scapy 
	dns_result = sr1(IP(dst="8.8.8.8")/UDP()/DNS(id=123,qr=0,opcode=0,rd=1,qd=DNSQR(qname=domain_name)), verbose=False)
    #Les id doivent être identique pour la enquête et la réponse.(qr=0: enquête) (opcode=0: standard) (rd=1: recherche récursive)
	layer = 0
	while True:#DNSRR peut avoir plusieurs couches
		try:
			#On garde seulement l'information sur l'Enregistre A
			if dns_result.getlayer(DNS).fields['an'][layer].fields['type'] == 1: 
				dns_result_ip = dns_result.getlayer(DNS).fields['an'][layer].fields['rdata']
				print('Domain Name: %s <==> IP address: %s' % (domain_name, dns_result_ip))
			layer += 1
		except:
			break


#Définissons des options
if __name__ == "__main__":
	parser = optparse.OptionParser('python3 DNS_Query.py --dn [Nom de domaine]')
	#Add une option "--dn" 
	parser.add_option('--dn', dest = 'domainName', type = 'string', help = 'le nom de domaine')
	(options, args) = parser.parse_args()
	domainName = options.domainName
	#Si la commande est sans option, on affiche l'example
	if domainName == None:
		print(parser.usage)
	else:
		#On effectue la fonction et affiche le résultat
		dns_query(domainName)

