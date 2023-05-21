import sys
import subprocess
import logging
import pickle

s = "vm"
lb = "lb"
n_lb = "1"
db = "db"
n_db = "1"
imagen = "ubuntu2004"
n_bridges = "2"
ip__db = "134.3.0.2"
ip0 = "134.3.0.1"
ip_inc = "134.3."
ip_end = ".1/24"
port = "8433"
port_serv = "8001"
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
		subprocess.run(["python3", "network.py", n_bridges, ip_inc, ip_end])
		# creación de la base de datos db y le asignamos su tarjeta a un bridge
		subprocess.run(["python3", "crear.py", db, imagen, n_db])
		subprocess.run(["python3", "networkconfig.py", db, n_db, ip__db])
		subprocess.run(["python3", "start.py", db, n_db])
		# creación de las máquinas virtuales y asignación de su tarjeta al bridge lxdbr0
		subprocess.run(["python3", "crear.py", s, imagen, parametros])
		subprocess.run(["python3", "networkconfig.py", s, parametros, ip0])
		# creación del balanceador de carga para redireccionar las peticiones de los clientes a los servidores para equilibrar la carga y ocultar al cliente la plataforma existentes de los servidores
		subprocess.run(["python3", "crear.py", lb, imagen, n_lb])
		subprocess.run(["python3", "eth.py", lb, n_lb])
		# Asignamos las tarjetas del contenedor lb a los bridges lxdbr1 & lxdbr0 y Asignamos sus direcciones IPv4:
		subprocess.run(["python3", "networkconfig.py", lb, n_bridges, ip_inc, n_lb])
		print("created!")
	
	elif orden == "start":
		subprocess.run(["sudo", "apt", "install", "xterm"])
		# iniciamos cada una de las máquinas virtuales ya creadas con el create
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		subprocess.run(["python3", orden+".py", s, numero])
		subprocess.run(["python3", orden+".py", lb, n_lb])		
		print("started!")

	elif orden == "list":
		# listado de las máquinas virtuales
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		subprocess.run(["python3", orden+".py", s, numero])
		subprocess.run(["python3", orden+".py", lb, n_lb])
		subprocess.run(["python3", orden+".py", db, n_db])
		subprocess.run(["lxc", orden])

	elif orden == "delete":
		subprocess.run(["python3", "pfinal2.py", "pause"])
		# delete de cada uno de las máquinas virtuales ya creadas con el create
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		subprocess.run(["python3", orden+".py", s, numero])
		subprocess.run(["python3", orden+".py", lb, n_lb])
		with open("remoto.txt", "rb") as fich:
			valor = pickle.load(fich)
		if valor == False:
			subprocess.run(["python3", orden+".py", db, n_db])
		else:
			subprocess.run(["python3", orden+".py", db, n_db])
		for i in range(int(n_bridges)-1):
			n = i + 1 
			subprocess.run(["lxc", "network", "delete", "lxdbr"+str(n)])
		print("deleted!")
		
	elif orden == "pause": # esta función pausa todos los contenedores creados al llamarla
		with open("numero.txt", "rb") as fich:
			numero = pickle.load(fich)
		subprocess.run(["python3", orden+".py", s, numero])
		subprocess.run(["python3", orden+".py", lb, n_lb])
		with open("remoto.txt", "rb") as fich:
			valor = pickle.load(fich)
		if valor == False:
			subprocess.run(["python3", orden+".py", db, n_db])
		else:
			subprocess.run(["remoto"])
		print("paused!")

	elif orden == "pauseone": # pausa la mv de valor parametros-1
		vm = sys.argv[2]
		parametros = sys.argv[3]
		nombre = vm + str(int(parametros)-1)
		subprocess.run(["lxc", "stop", nombre, "--force"])
		print("paused "+nombre+"!")

	elif orden == "configure": # configura el servicio web (app en servidores y base de datos en db) + el balanceador
		try:
			IP_B = sys.argv[2]
			subprocess.run(["python3", "ipremoto.py"])
			with open("ip_remoto.txt", "rb") as fich:
				IP_A = picle.load(fich)
			fich.close()
			with open("remoto.txt", "wb") as fich:
				pickle.dump(True, fich)
			with open("ipdb.txt", "wb") as ipdb:
				pickle.dump(ip-B, ipdb)
			subprocess.run(["python3", "configureremoto.py", db, n_db, ip_B, port, ip_inc+"0"+ip_end, IP_A, lxdbr_remoto])
		except IndexError:
			with open("remoto.txt", "wb") as fich:
				pickle.dump(False, fich)
			subprocess.run(["python3", "configure.py", db, n_db])

		subprocess.run(["python3", "configure_servidores.py", s, ip0])
		subprocess.run(["python3", "configure_lb.py", lb, n_lb, s, port_serv])
		print("configured!")
	else:
		# error del parámetro orden
		logger.error("el argumento orden => " + orden + " no es correcto")
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
