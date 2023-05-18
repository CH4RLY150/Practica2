import sys
import subprocess
import logging
import pickle

nom_imagen = "image_server"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	orden = sys.argv[1]
	parametros = sys.argv[2]
	
	subprocess.run(["python3", "start.py", orden, parametros])
	for i in range(int(parametros)):
		nombre = orden + str(i)
		subprocess.run(["lxc", "exec", nombre, "--", "apt", "update"])
		subprocess.run(["lxc", "exec", nombre, "--", "apt","install", "haproxy"])
		with open("numero.txt", "rb") as nvm:
			numero = pickle.load(nvm)
		with open("hola.cfg", "r+") as hapro:
			lines = hapro.readlines()
		with open("haproxy.cfg", "w") as hapro:
			hapro.writelines(lines)
			for i in range(int(numero)):
				nombre = s + str(i)
				hapro.writelines("	server webserver" + str(i+1) + " " + nombre + ":"+port+"\n")
				hapro.writelines("        option httpchk")
		subprocess.run(["lxc", "file", "push", "haproxy.cfg", nombre+"/etc/haproxy/haproxy.cfg"])
	subprocess.run(["python3", "pfinal2.py", "pauseone", lb, parametros])
	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
