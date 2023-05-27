import sys
import subprocess
import logging
import pickle

IP_lb = ".10"
lxdbr0 = "lxdbr0"
lxdbr1 = "lxdbr1"
lxdbr = "lxdbr"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def networkconfig(orden, parametros, ip1, n_lb):
	try:
		# Asignamos cada servidor al bridge lxdbr0 y asignamos su dirección IPv4:
		if orden == "lb":
			for j in range(int(n_lb)):
				if n_lb == "1":
					nombre = orden
				else:
					nombre = orden + str(j)
				for i in range(int(parametros)):
					subprocess.run(["lxc", "network", "attach", lxdbr+str(i), nombre, "eth"+str(i)])
					subprocess.run(["lxc", "config", "device", "set", nombre, "eth"+str(i), "ipv4.address", ip1 + str(i) + IP_lb])
		elif orden == "s":
			for i in range(int(parametros)):
				nombre = orden + str(i)
				m = i+1
				subprocess.run(["lxc", "network", "attach", lxdbr0, nombre, "eth0"])
				subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", ip1 + str(m)])
		elif orden == "db":
			for i in range(int(parametros)):
				if parametros == "1":
					nombre = orden
				else:
					nombre = orden + str(j)
				subprocess.run(["lxc", "network", "attach", lxdbr0, nombre, "eth0"])
				subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", ip1 + str(i)])
				with open("ip_db.txt", "wb") as fich:
					pickle.dump(ip1 + str(i), fich)
		elif orden == "cl":
			for i in range(int(parametros)):
				if parametros == "1":
					nombre = orden
				else:
					nombre = orden + str(j)
				subprocess.run(["lxc", "network", "attach", lxdbr1, nombre, "eth0"])
				subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", ip1 + str(i+1)])
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
