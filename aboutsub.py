import requests
import socket
import threading
import time
import optparse

speed = threading.BoundedSemaphore(value=20)
def getOpenedPorts(ip,lop):
	if lop == []:
		print('http://www.{} Ok'.format(ip))
	else:
		ports = []
		speed.acquire()
		for p in lop:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			scanOnp = s.connect_ex((socket.gethostbyname(ip), p))
			if scanOnp == 0:
				ports.append(p)
			s.close()
		
		print('{}\nports : {}'.format(ip+' Ok ',ports))
		print('------------------------')

def Chec_if_200L(listop, port):
	if port != []:
		port = list(map(int, port.split(',')))
	try:
		f = open(listop,'r')
		for i in f.readlines():
			try:
				if requests.get('http://{}'.format(i.strip('\n'))).status_code == 200:
					#port = list(map(int, port.split(',')))
					th = threading.Thread(target=getOpenedPorts, args=(i.strip('\n'),port))
					th.start()
				else:
					print(i.strip('\n'), requests.get('http://www.{}'.format(i.strip('\n'))).status_code)

			except requests.exceptions.ConnectionError: pass
			except requests.exceptions.MissingSchema: pass
			except requests.exceptions.InvalidURL: pass
	except FileNotFoundError:
		print('The file is not excest!')
		exit()

def Chec_if_200S(url, port):
	if port != []:
		port = list(map(int, port.split(',')))
	try:
		#requests.get('http://www.{}'.format(url)).status_code
		if requests.get('http://{}'.format(url)).status_code == 200:
			th = threading.Thread(target=getOpenedPorts, args=(url,port))
			th.start()
		else:
			print(url, 'No')

	except requests.exceptions.ConnectionError: pass
	except requests.exceptions.MissingSchema: pass
	except requests.exceptions.InvalidURL: pass



#URLs = input('Enter your word list : ')
#port = list(map(int, input('Enter list of ports : ').split()))

#if len(port) == 0:
#	print('no ports excets')
#	exit()

parse = optparse.OptionParser('''


   __    ____  _____  __  __  ____  ___  __  __  ____ 
  /__\  (  _ \(  _  )(  )(  )(_  _)/ __)(  )(  )(  _ \
 /(__)\  ) _ < )(_)(  )(__)(   )(  \__ \ )(__)(  ) _ <
(__)(__)(____/(_____)(______) (__) (___/(______)(____/

	Note: dont use :
		'https://www.domain.com or https://www.subdomain.com' 

	-p 			To also test ports in subdomains
	-l 			List of subdomains you want to scan
	-s 			To scan single subdomain

	''')
parse.add_option('-p',dest="port",default=[])

parse.add_option('-l',dest="listsd")

parse.add_option('-s',dest="singelsub")

(op , args) = parse.parse_args()

if op.listsd == None and op.singelsub == None:

	print(parse.usage)

	print('you must uose ( -l or -s ) to start scan')

elif op.listsd != None:

	print('this may take a while')
	time.sleep(2)

	Chec_if_200L(op.listsd, op.port)

elif op.singelsub != None:

	print('this may take a while')
	time.sleep(2)

	Chec_if_200S(op.singelsub, op.port)

	

