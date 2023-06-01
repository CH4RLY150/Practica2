import sys
import subprocess
import pickle

def guess_ip(var):
	if var == "A":
		local = subprocess.getoutput("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1 | awk '{print $2}'")
		with open("ip_remoto.txt", "w") as fich:
			fich.writelines(local)
		fich.close()
		with open("ip_remoto.txt", "r+") as fich:
			lines = fich.readlines()
		fich.close()
		IP = lines[1]
		N = len(IP)
		IP_ = IP[0:N-1]
		print("la ip de la máquina es: "+IP_)
	else:
		local = subprocess.run(["dig", "+noauthority", "+noadditional", var+".lab.dit.upm.es"], stdout = subprocess.PIPE)
		with open("ip_remoto.txt", "w") as fich:
			fich.writelines(local.stdout.decode("utf-8"))
		fich.close()
		with open("ip_remoto.txt", "r+") as fich:
			lines = fich.readlines()
		fich.close()
		IP = lines[14-1]
		N = len(IP)
		IP_ = IP[31:N-1]
		print("la ip de la máquina remota "+var+" es: "+IP_)
	return IP_
