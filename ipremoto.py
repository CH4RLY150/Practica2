import sys
import subprocess
import pickle

def ipremoto():
	local = subprocess.getoutput("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1| awk '{print $2}'")

	with open("ip_remoto.txt", "w") as fich:
		fich.writelines(local)
	fich.close()
	with open("ip_remoto.txt", "r+") as fich:
		lineas = fich.readlines()
	fich.close()
		IP = lineas[1]
	N = len(IP) 
	IP_ = IP[0:N-1]
	with open("ip_remoto.txt", "wb") as fich:
		pickle.dump(IP_, fich)
