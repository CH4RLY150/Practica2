import sys
import subprocess
import logging
import pickle

IP_lb = ".10"
lxdbr0 = "lxdbr0"
lxdbr1 = "lxdbr1"
lxdbr = "lxdbr"
eth0 = "eth0"
eth1 = "eth1"
ip_ini = "134.3."
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
#Función que asigna la ip a los contenedores:
#Parámeros:
#	nom_cont: nombre del contenedor
#	n_ser: número de servidores

def networkconfig(nom_cont, n_ser):
	print("Asignando ip a " + nom_cont)
	if nom_cont == "lb":
		subprocess.run(["lxc", "stop", nom_cont])
		subprocess.run(["lxc", "network", "attach", lxdbr0, nom_cont, eth0])
		subprocess.run(["lxc", "config", "device", "set", nom_cont, eth0, "ipv4.address", ip_ini + "0.10"])
		subprocess.run(["lxc", "network", "attach", lxdbr1, nom_cont, eth1])
		subprocess.run(["lxc", "config", "device", "set", nom_cont, eth1, "ipv4.address", ip_ini + "1.10"])
	elif nom_cont == "db":
		subprocess.run(["lxc", "stop", nom_cont])
		subprocess.run(["lxc", "network", "attach", lxdbr0, nom_cont, eth0])
		subprocess.run(["lxc", "config", "device", "set", nom_cont, eth0, "ipv4.address", ip_ini + "0.20"])
	elif nom_cont == "s":
		for i in range(int(n_ser)):
			n = i + 1 
			server = nom_cont + str(n)
			ip = ip_ini + "0.1" + str(n)
			print(server)
			print(ip)
			subprocess.run(["lxc", "stop", server])
			subprocess.run(["lxc", "network", "attach", lxdbr0, server, eth0])
			subprocess.run(["lxc", "config", "device", "set", server, eth0, "ipv4.address", ip])			
	elif nom_cont == "cl":
		subprocess.run(["lxc", "stop", nom_cont])
		subprocess.run(["lxc", "network", "attach", lxdbr0, nom_cont , eth1])
		subprocess.run(["lxc", "config", "device", "set", nom_cont, eth1, "ipv4.address", ip_ini + "1.11"])
	print("Ip asignada a " + nom_cont)
