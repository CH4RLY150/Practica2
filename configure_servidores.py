import time
import sys
import subprocess
import logging
import pickle
import pause

nom_imagen = "image_server"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def configure_servidores(vm, ip0, lxdbr0):
	try:
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)

		#configuración de servidores
		with open("nom_imagen.txt", "rb") as fich:
			imagen_s = pickle.load(fich)

		for i in range(int(numero)-1):
			nombre = vm + str(i+1)
			subprocess.run(["lxc", "init", imagen_s, nombre])
			m = i+2
			subprocess.run(["lxc", "network", "attach", lxdbr0, nombre, "eth0"])
			subprocess.run(["lxc", "config", "device", "set", nombre, "eth0", "ipv4.address", ip0 + str(m)])
			
		
		#subprocess.run(["python3", "crear.py", vm, "1"])
		#subprocess.run(["python3", "networkconfig.py", vm, "1"])
		#nombre = vm + str(0)
		#subprocess.run(["lxc", "start", nombre])	
		#time.sleep(5)	
		#subprocess.run(["lxc", "file", "push", "install.sh", nombre+"/root/install.sh"])
		#subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])
		#subprocess.run(["lxc", "file", "push", "-r", "app", nombre+"/root"])
		#subprocess.run(["lxc", "exec", nombre, "--", "./install.sh"])
		#subprocess.run(["lxc", "restart", nombre])
		#subprocess.run(["lxc", "publish", nombre, "--alias", nom_imagen])
		#subprocess.run(["python3", "crear.py", s, nom_imagen, numero])
		#subprocess.run(["python3", "networkconfig.py", s, numero, ip1])
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
