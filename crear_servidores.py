import sys
import subprocess
import time
import pickle

def crear_servidores(orden, imagen, parametros):
	with open("ip_db.txt", "rb") as ipdb:
		ip = pickle.load(ipdb)
		
	#determinar el ip de la DB en app
	lines = list()
	with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "r+") as fichero:
		lines = fichero.readlines()
		lines[3-1]="const mongoURL = process.env.MONGO_URL || 'mongodb://"+ip+":27017/bio_bbdd';\n"
	fichero.close()
	with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "w") as files:
		files.writelines(lines)
	files.close()
	with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "r+") as fichero:
		lines = fichero.readlines()
		lines[12-1]="    await mongoose.connect('mongodb://"+ip+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })\n"
	with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "w") as files:
		files.writelines(lines)
	
	with open("nom_imagen.txt", "rb") as ficheros:
		nom_imagen = pickle.load(ficheros)
	ficheros.close()
	
	nombre = orden + str(0)
	subprocess.run(["lxc", "init", imagen, nombre])
	subprocess.run(["lxc", "start", nombre])		
	time.sleep(5)
	subprocess.run(["lxc", "file", "push", "install.sh", nombre+"/root/install.sh"])
	subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])
	subprocess.run(["lxc", "file", "push", "-r", "app", nombre+"/root"])
	subprocess.run(["lxc", "exec", nombre, "--", "./install.sh"])
	subprocess.run(["lxc", "restart", nombre])
	subprocess.run(["lxc", "stop", nombre])
	subprocess.run(["lxc", "publish", nombre, "--alias", nom_imagen])
	with open("nom_imagen.txt", "wb") as fich:
		pickle.dump(nom_imagen, fich)
