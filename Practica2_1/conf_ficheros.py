import sys
import subprocess
import time
import pickle


def conf_ficheros(orden,ip):
		
	#determinar el ip de la DB en app
	
	lines = list()
	if orden == db:
		with open("app/md-seed-config.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[3-1]="const mongoURL = process.env.MONGO_URL || 'mongodb://"+ip+":27017/bio_bbdd';\n"
		fichero.close()
		with open("app/md-seed-config.js", "w") as files:
			files.writelines(lines)
		files.close()
	elif orden == ip_rem:
		with open("app/rest_server.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[12-1]="    await mongoose.connect('mongodb://"+ip+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })\n"
		with open("app/rest_server.js", "w") as files:
			files.writelines(lines)
	
		with open("nom_imagen.txt", "rb") as ficheros:
			nom_imagen = pickle.load(ficheros)
