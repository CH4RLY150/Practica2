import sys
import subprocess
import logging
import pickle
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def configure_lb(orden, parametros, s, port):
	try:
		with open("numero.txt", "rb") as nvm:
			numero = pickle.load(nvm)
		nvm.close()
		for i in range(int(parametros)):
			if parametros == "1":
				nombre_1 = orden
			else:
				nombre_1 = orden + str(i)
			subprocess.run(["lxc", "start", nombre_1])
			time.sleep(5)
			subprocess.run(["lxc", "exec", nombre_1, "--", "apt", "update"])
			subprocess.run(["lxc", "exec", nombre_1, "--", "apt","install", "-y", "haproxy"])
			
			with open("hola.cfg", "r+") as hapro:
				lines = hapro.readlines()
			hapro.close()
			with open("haproxy.cfg", "w") as hapro:
				hapro.writelines(lines)
				for i in range(int(numero)):
					nombre = s + str(i)
					hapro.writelines("	server webserver" + str(i+1) + " " + nombre + ":"+port+"\n")
				hapro.writelines("        option httpchk")
			subprocess.run(["lxc", "file", "push", "haproxy.cfg", nombre_1+"/etc/haproxy/haproxy.cfg"])
		subprocess.run(["python3", "pfinal2.py", "pauseone", orden, parametros])
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
