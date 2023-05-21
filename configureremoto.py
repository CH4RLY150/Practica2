import sys
import subprocess
import logging
import pickle

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	# conectamos los servidores con una DDBB remota
			#db$ ip addr show
			#db$ lxc config set core.https_address IP-B:8443
			#db$ lxc config set core.trust_password mypass
	db = sys.argv[1]
	parametros = sys.argv[2]
	ip_addr = sys.argv[3]
	port = sys.argv[4]
	ip_ = sys.argv[5]
	IP_A = sys.argv[6]
	lxdbr = sys.arv[7]
	sentencia = ip_addr + ":" + port
	#configuración del remoto
	subprocess.run(["lxc", "config", "set", "core.https_address", IP_A+":"+port])
	subprocess.run(["lxc", "remote", "add", "remoto"+db, ip_addr+":"+port, "--password", "mypass", "--accept-certificate"])
	#configuración de red y bridges
	subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.addres", ip_])
	subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.nat", "true" ])
	#configuración de la base de datos remota
	subprocess.run(["python3", "configure.py", db, parametros])
	for i in range(int(parametros)):
		nombre = db + str(i)
		subprocess.run(["lxc", "copy", nombre, "remoto"+db+":"+nombre])
		subprocess.run(["lxc", "start", "remoto"+db+":"+nombre])
	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
