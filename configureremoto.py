import sys
import subprocess
import logging
import pickle

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def configureremoto(db, parametros, IP_B, port, ip_, lxdbr, IP_A, password, s):
	try:
		# conectamos los servidores con una DDBB remota
			#db$ ip addr show
			#db$ lxc config set core.https_address IP-B:8443
			#db$ lxc config set core.trust_password mypass
		#configuración del remoto
		subprocess.run(["lxc", "config", "set", "core.https_address", IP_A+":"+port])
		subprocess.run(["lxc", "remote", "add", "remoto"+db, IP_B+":"+port, "--password", password, "--accept-certificate"])
		#configuración de red y bridges
		subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.addres", ip_])
		subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.nat", "true" ])
		for i in range(int(parametros)):
			if parametros == "1":
				nombre = db
			else:
				nombre = db + str(i)
			subprocess.run(["lxc", "stop", nombre])
			subprocess.run(["lxc", "copy", nombre, "remoto"+db+":"+nombre])
			subprocess.run(["lxc", "start", "remoto"+db+":"+nombre])
			subprocess.run(["lxc", "delete", nombre])
		
		# actualizamos la ip de la db a la IP de la nueva db remota (que es la IP-B)
		# para ello debemos cambiar los documentos de la app instalada en cada servidor 
		lines = list()
		with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[3-1]="const mongoURL = process.env.MONGO_URL || 'mongodb://"+IP_B+":27017/bio_bbdd';\n"
		fichero.close()
		with open("/home/c.mbarros/Práctica_2/app/md-seed-config.js", "w") as files:
			files.writelines(lines)
		files.close()
		with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[12-1]="    await mongoose.connect('mongodb://"+IP_B+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })\n"
		with open("/home/c.mbarros/Práctica_2/app/rest_server.js", "w") as files:
			files.writelines(lines)
		files.close()
		with open("numero.txt", "rb") as files:
			numero = pickle.load(files)
		for i in range(int(numero)):
			nombre = s + str(i)
			subprocess.run(["lxc", "push", "/home/c.mbarros/Práctica_2/app/md-seed-config.js", nombre+"/app/md-seed-config.js"])
			subprocess.run(["lxc", "push", "/home/c.mbarros/Práctica_2/app/rest_server.js", nombre+"/app/rest_server.js"])
			
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
