import sys
import subprocess
import logging
import pickle
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def configure_lb(orden, parametros, s, port):
	try:
		fich = open("numero.txt","r")
		num = fich.read()
		fich.close()
		
		subprocess.run(["lxc", "start", orden])
		time.sleep(5)
		subprocess.run(["lxc", "exec", orden, "--", "apt", "update"])
		subprocess.run(["lxc", "exec", orden, "--", "apt","install", "-y", "haproxy"])
		with open("hola.cfg", "r+") as hapro:
			lines = hapro.readlines()
		hapro.close()
		with open("haproxy.cfg", "w") as hapro:
			hapro.writelines(lines)
			for i in range(int(num)):
				nombre = s + str(i+1)
				hapro.writelines("	server webserver" + str(i+1) + " " + nombre + ":"+port+"\n")
			hapro.writelines("        option httpchk")
		subprocess.run(["lxc", "file", "push", "haproxy.cfg", orden+"/etc/haproxy/haproxy.cfg"])
		subprocess.run(["python3", "pfinal2.py", "pauseone", orden, parametros])
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
