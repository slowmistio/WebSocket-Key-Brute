#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# by Momo Outaadi (m4ll0k)
# for more information https://tools.ietf.org/html/rfc6455

import sys
import base64
import urllib3
import requests
import threading

lock = threading.Lock()

R  = "\033[0;31m"
G  = "\033[0;32m"  
Y  = "\033[0;33m"  
E  = "\033[0m"  
RR = "\033[1;31m"
GG = "\033[1;32m"

def plus(STR):print('%s[+]%s %s'%(GG,STR,E))
def info(STR):print('%s[i]%s %s'%(Y,STR,E))
def warn(STR):print('%s[!]%s %s'%(RR,STR,E))

def usage():
	print("\nUsage: %s http://[target]:port wordlist.txt\n"%(sys.argv[0]))
	print("\t- %s http://site.com:8080/ wordlist.txt"%(sys.argv[0]))
	print('--'*30)
	exit(0)

def readfile():return[l.strip() for l in open(sys.argv[2],'rb')]
def main():
	headers = {
				'Upgrade'               : 'websocket',
				'Connection'            : 'Upgrade',
				'Sec-WebSocket-Protocol': 'chat, superchat',
				'Sec-WebSocket-Version' : '13',
	}
	session = requests.session()
	request = requests.packages.urllib3.disable_warnings(
		urllib3.exceptions.InsecureRequestWarning
		)
	info(' Loading %s words...'%(len(readfile())))
	info(' Handshake...')
	for passwd in readfile():
		headers['Sec-WebSocket-Key'] = base64.b64encode(passwd)
		request = session.request(method="GET",url=sys.argv[1],headers=headers)
		if request.status_code == 101 and request.headers['Sec-WebSocket-Accept']:
			plus(' Valid Key..')
			print('    - %s (%s)'%(headers['Sec-WebSocket-Key'],
				base64.b64decode(headers['Sec-WebSocket-Key'])))
			exit()
		else:
			sys.stdout.write('\r%s[!] Invalid Key: %s%s%s'%(R,RR,headers['Sec-WebSocket-Key'],E))
			sys.stdout.flush()
	print('')
	warn(' Wasn\'t found any KEY!!')

try:
	if len(sys.argv) < 3: usage()
	threads = []
	for i in range(0,1):
		task = threading.Thread(target=main, args=())
		threads.append(task)
	# start
	for thread in threads:
		thread.start()
	# join
	for thread in threads:
		thread.join()
except Exception as e:
	usage()