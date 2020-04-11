#!/usr/bin/env python3


# imports

import requests
import socket
import threading
import time
import optparse

# variables

headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
sema = threading.BoundedSemaphore(value=20)

# lambda

req = lambda url : requests.get(url, headers=headers)


# functions

def getOpenedPorts(ip,lop):

	if lop == []:
		data = 'url : https://www.{}\nstatus : {}\nalive : Ok'.format(ip, req('https://{}'.format(ip)).status_code)
	else:
		ports = []
		sema.acquire()
		for p in lop:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(2)

			scanOnp = s.connect_ex((socket.gethostbyname(ip), p))
			if scanOnp == 0:
				ports.append(p)
			s.close()
		
		data = 'url : https://www.{}\nstatus : {}\nports : {}\nalive : Ok'.format(ip, req('https://{}'.format(ip)).status_code,list(set(ports)))
	print(data)	
	print('------------------------')



def Chec_if_200S(url, port):
	url = url.strip('\n')
	if port != []:
		port = list(map(int, port.split(',')))
	try:
		if 'http' in url or 'https' in url:
			url = url.lstrip('http://www.').lstrip('https://www.')


		if req('https://{}'.format(url)).status_code == 200:
			th = threading.Thread(target=getOpenedPorts, args=(url,port))
			th.start()
		else:
			print('url : https://www.{}'.format(url))
			print('status : {}\nalive : no'.format(req('https://{}'.format(url)).status_code))
			print('------------------------')

	except requests.exceptions.ConnectionError:
		print('No URL Named : http://{}'.format(url))
		print('------------------------')
	except requests.exceptions.SSLError:
		print('SSL Certificate Error')
		print('------------------------')





parse = optparse.OptionParser('''


   __    ____  _____  __  __  ____  ___  __  __  ____ 
  /__\  (  _ \(  _  )(  )(  )(_  _)/ __)(  )(  )(  _ \
 /(__)\  ) _ < )(_)(  )(__)(   )(  \__ \ )(__)(  ) _ <
(__)(__)(____/(_____)(______) (__) (___/(______)(____/

	Note: dont use :
		'http://www.domain.com or https://www.subdomain.com' 

	-p 			To also test ports in subdomains
	-l 			List of subdomains you want to scan
	-s 			To scan single subdomains

	''')
parse.add_option('-p',dest="port",default=[])

parse.add_option('-l',dest="listsd")

parse.add_option('-s',dest="singelsub")

(op , args) = parse.parse_args()


print('this may take a while\n')
time.sleep(2)

# Driver Code 


if op.listsd == None and op.singelsub == None:

	print(parse.usage)

	print('you must uose ( -l Or -s ) to start scan')

elif op.listsd != None:

	try:
		f = open(op.listsd, 'r')
		for i in f.readlines():
			Chec_if_200S(i, op.port)

	except FileNotFoundError:
		print('The file is not Exist!')
		exit()


elif op.singelsub != None:


	Chec_if_200S(op.singelsub, op.port)

	
