import sys
import subprocess
import logging
import pickle
import time
import start
import red
import crear
import networkconfig
import eth
import lista
import delete
import pause
import configure
import configureremoto
import configure_servidores
import configure_lb
import delete_remoto
import pause_remoto
import ipremoto

s = "s"
lb = "lb"
n_lb = "1"
db = "db"
n_db = "1"
c1 = "cl"
n_c1 = "1"
imagen = "ubuntu2004"
n_bridges = "2"
ip__db = "134.3.0.2"
ip1 = "134.3.1.1"
ip0 = "134.3.0.1"
ip_inc = "134.3."
ip_end = ".1/24"
port = "8433"  #puerto en el que escucha lxd
port_serv = "8001"   # especificado por el código en app
lxdbr_ = "lxdbr"
lxdbr0 = "lxdbr0"
lxdbr_remoto = "lxdbr0"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
# configuramos el lxd
	# sudo usermod -a -G lxd $USER
	# newgrp lxd
subprocess.run(["lxd", "init", "--auto"])
# ver el contenido del fichero en la consola de comandos
	# cat pfinal2.py

try:
	orden = sys.argv[1] 
	if orden == "create":
		subprocess.run(["lxc", "image", "import", "/mnt/vnx/repo/arso/ubuntu2004.tar.gz", "--alias", imagen])
		try:
			parametros = sys.argv[2]
			#comprobación del argumento parametros
			if int(parametros) <= 5 and int(parametros) > 0:
				print("segundo argumento correcto")
			else:
				logger.error("el número introducido: " + parametros + "como segundo argumento no es correcto")
				raise IndexError
		except IndexError:
			parametros = "2"
		with open("numero.txt", "wb") as fich:
			pickle.dump(parametros, fich)
		# creación de los bridges virtuales y asignación de IP (subred)
		red.red(n_bridges, ip_inc, ip_end, lxdbr_)
		# creación de la base de datos db y le asignamos su tarjeta a un bridge
		crear.crear(db, imagen, n_db)
		networkconfig.networkconfig(db, n_db, ip__db, n_lb)
		start.start(db, n_db)
		time.sleep(5)
		configure.configure(db, n_db)
		# creación de las máquinas virtuales y asignación de su tarjeta al bridge lxdbr0
		crear.crear(s, imagen, parametros)
		networkconfig.networkconfig(s, "1", ip0, n_lb)
		# creación del balanceador de carga para redireccionar las peticiones de los clientes a los servidores para equilibrar la carga y ocultar al cliente la plataforma existentes de los servidores
		crear.crear(lb, imagen, n_lb)
		eth.eth(lb, n_lb)
		# Asignamos las tarjetas del contenedor lb a los bridges lxdbr1 & lxdbr0 y Asignamos sus direcciones IPv4:
		networkconfig.networkconfig(lb, n_bridges, ip_inc, n_lb)
		# creación de los clientes
		crear.crear(c1, imagen, n_c1)
		networkconfig.networkconfig(c1, n_c1, ip1, n_lb)
		print("created!")
	
	elif orden == "start":
		subprocess.run(["sudo", "apt", "install", "xterm"])
		# iniciamos cada una de las máquinas virtuales ya creadas con el create
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		start.start(s, numero)
		start.start(lb, n_lb)	
		start.start(c1, n_c1)	
		print("started!")

	elif orden == "list":
		# listado de las máquinas virtuales
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		lista.lista(s, numero)
		lista.lista(lb, n_lb)
		lista.lista(db, n_db)
		lista.lista(c1, n_c1)
		subprocess.run(["lxc", orden])

	elif orden == "delete":
		subprocess.run(["python3", "pfinal2.py", "pause"])
		# delete de cada uno de las máquinas virtuales ya creadas con el create
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		delete.delete(s, numero)
		delete.delete(lb, n_lb)
		delete.delete(c1, n_c1)
		with open("remoto.txt", "rb") as fich:
			valor = pickle.load(fich)
		if valor == False:
			delete.delete(db, n_db)
		else:
			delete_remoto.delete_remoto(db, n_db)
		for i in range(int(n_bridges)-1):
			n = i + 1 
			subprocess.run(["lxc", "network", "delete", lxdbr_+str(n)])
		print("deleted!")
		
	elif orden == "pause": # esta función pausa todos los contenedores creados al llamarla
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		pause.pause(s, numero)
		pause.pause(lb, n_lb)
		pause.pause(c1, n_c1)
		with open("remoto.txt", "rb") as fich:
			valor = pickle.load(fich)
		if valor == False:
			pause.pause(db, n_db)
		else:
			pause_remoto.pause_remoto(db, n_db)
		print("paused!")

	elif orden == "pauseone": # pausa la mv de valor parametros-1
		var = sys.argv[2]
		parametros = sys.argv[3]
		if orden == s:
			nombre = vm + str(int(parametros)-1)
		elif parametros == "1":
			nombre = var
		else:
			nombre = var + str(int(parametros)-1)
		subprocess.run(["lxc", "stop", nombre, "--force"])
		print("paused "+nombre+"!")

	elif orden == "configure": # configura el servicio web (app en servidores y base de datos en db) + el balanceador
		configure_servidores.configure_servidores(s, ip0, lxdbr0)
		try:
			lB = sys.argv[2] # l212 por ejemplo
			password = sys.argv[3] # contraseña del remoto en el LXC del remotodb
			IP_B = ipremoto.guess_ip(lB)
			IP_A = ipremoto.guess_ip("A")
			with open("remoto.txt", "wb") as fich:
				pickle.dump(True, fich)
			with open("ipdb.txt", "wb") as ipdb:
				pickle.dump(IP_B, ipdb)
			configureremoto.configureremoto(db, n_db, IP_B, port, ip_inc+"0"+ip_end, lxdbr_remoto, IP_A, password, s)
		except IndexError:
			with open("remoto.txt", "wb") as fich:
				pickle.dump(False, fich)

		configure_lb.configure_lb(lb, n_lb, s, port_serv)
		print("configured!")
	else:
		# error del parámetro orden
		logger.error("el argumento orden => " + orden + " no es correcto")
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
