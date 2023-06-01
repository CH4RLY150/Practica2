import sys
import subprocess
import logging
import pickle
import time
import crear_servidores
import crear_servers

nom_imagen = "nuevaImagen"

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

#Función que crea los contenedores:
#Parámeros:
#	nom_cont: nombre del contenedor
#	imagen: imagen del contenedor
#	n_ser: número de servidores

def crear(nom_cont, imagen, n_ser):
	if nom_cont == "db" or nom_cont == "lb" or nom_cont == "cl":
		print("Creando contenedor " + nom_cont)
		subprocess.run(["lxc", "init", imagen, nom_cont])
		print("Contenedor " + nom_cont + " creado")
	elif nom_cont == "s":
		for i in range(int(n_ser)):
			server = nom_cont + str(i+1)
			print("Creando contenedor " + server)
			crear_servers.crear_servers(server)
			subprocess.run(["lxc","exec",server,"--","forever","start","app/rest_server.js"])
			print("Contenedor " + server + " creado")
			
	
