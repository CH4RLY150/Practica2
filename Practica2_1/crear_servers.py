import sys
import subprocess
import logging
import pickle
import time

imagen_nueva = "imagen_base"
imagen = "ubuntu:20.04"
#Función que crea el servidor 1, una imagen de este y los otros contenedores a partir de la imagen:
#Parámeros:
#	server: servidor a crear
def crear_servers(server):
	if server == "s1":
		subprocess.run(["lxc", "init", imagen, server])
		print("Creando imagen de " + server)
	
		with open("nom_imagen.txt", "rb") as ficheros:
			nom_imagen = pickle.load(ficheros)
		ficheros.close()
		subprocess.run(["lxc", "start", server])		
		time.sleep(5)
		subprocess.run(["lxc", "file", "push", "install.sh", server+"/root/install.sh"])
		subprocess.run(["lxc", "exec", server, "--", "chmod", "+x", "install.sh"])
		subprocess.run(["lxc", "file", "push", "-r", "app", server+"/root"])
		subprocess.run(["lxc", "exec", server, "--", "./install.sh"])
		subprocess.run(["lxc", "restart", server])
		subprocess.run(["lxc", "stop", server])
		subprocess.run(["lxc", "publish", server, "--alias", imagen_nueva])
		print("Imagen creada")
	else:
		subprocess.run(["lxc", "init", imagen_nueva, server])
	
	
