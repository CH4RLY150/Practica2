import sys
import subprocess
import logging
import pickle
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	orden = sys.argv[1]
	parametros = sys.argv[2]
	s = sys.argv[3]
	port = sys.argv[4]
	
	for i in range(int(parametros)):
		nombre = orden + str(i)
		subprocess.run(["lxc", "start", nombre])
		time.sleep(5)
		subprocess.run(["lxc", "exec", nombre, "--", "apt", "update"])
		subprocess.run(["lxc", "exec", nombre, "--", "apt","install", "haproxy"])
		with open("numero.txt", "rb") as nvm:
			numero = pickle.load(nvm)
		nvm.close()
		with open("hola.cfg", "r+") as hapro:
			lines = hapro.readlines()
		hapro.close()
		with open("haproxy.cfg", "w") as hapro:
			hapro.writelines(lines)
			for i in range(int(numero)):
				nombre = s + str(i)
				hapro.writelines("	server webserver" + str(i+1) + " " + nombre + ":"+port+"\n")
			hapro.writelines("        option httpchk")
		subprocess.run(["lxc", "file", "push", "haproxy.cfg", nombre+"/etc/haproxy/haproxy.cfg"])
		subprocess.run(["python3", "pfinal2.py", "pauseone", orden, str(int(parametros)+1)])
	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
